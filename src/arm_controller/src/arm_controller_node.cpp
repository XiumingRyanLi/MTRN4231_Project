#include <memory>
#include <thread>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"

#include "geometry_msgs/msg/pose.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "moveit/planning_scene_interface/planning_scene_interface.h"
#include "moveit_msgs/msg/collision_object.hpp"
#include "moveit_msgs/msg/constraints.hpp"
#include "moveit_msgs/msg/orientation_constraint.hpp"
#include "shape_msgs/msg/solid_primitive.hpp"

#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>

#include "custom_interfaces/action/move_tcp.hpp"

using MoveTCP = custom_interfaces::action::MoveTCP;
using GoalHandleMoveTCP = rclcpp_action::ServerGoalHandle<MoveTCP>;

class ArmController
{
public:
  explicit ArmController(const rclcpp::Node::SharedPtr& node)
  : node_(node),
    tf_buffer_(node_->get_clock()),
    tf_listener_(tf_buffer_)
  {
    RCLCPP_INFO(node_->get_logger(), "Starting ArmController with MoveIt…");

    // MoveGroupInterface like the working server: node_ is a real shared_ptr
    move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
        node_, "ur_manipulator",
        std::shared_ptr<tf2_ros::Buffer>(),
        rclcpp::Duration::from_seconds(5.0));

    // Planner & timing to match your style
    node_->declare_parameter("planning_time", 15.0);
    node_->declare_parameter("goal_joint_tolerance", 0.005);
    node_->declare_parameter("goal_position_tolerance", 0.005);
    node_->declare_parameter("goal_orientation_tolerance", 0.005);

    move_group_->setPlanningTime(node_->get_parameter("planning_time").as_double());
    move_group_->setGoalJointTolerance(node_->get_parameter("goal_joint_tolerance").as_double());
    move_group_->setGoalPositionTolerance(node_->get_parameter("goal_position_tolerance").as_double());
    move_group_->setGoalOrientationTolerance(node_->get_parameter("goal_orientation_tolerance").as_double());
    move_group_->setPlannerId("RRTConnect");      // consistent with your working server
    move_group_->setMaxVelocityScalingFactor(0.25);
    move_group_->setMaxAccelerationScalingFactor(0.25);

    setupCollisionObjects();

    // Action server — your type + your route
    action_server_ = rclcpp_action::create_server<MoveTCP>(
      node_.get(),
      "/arm/pick_place",
      std::bind(&ArmController::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&ArmController::handle_cancel, this, std::placeholders::_1),
      std::bind(&ArmController::handle_accepted, this, std::placeholders::_1));

    RCLCPP_INFO(node_->get_logger(),
                "Ready. Group=%s, EEF=%s, planning frame=%s",
                move_group_->getName().c_str(),
                move_group_->getEndEffectorLink().c_str(),
                move_group_->getPlanningFrame().c_str());
  }

private:
  // ---------------- Action plumbing (same pattern as your attempt) ----------------
  rclcpp_action::GoalResponse handle_goal(const rclcpp_action::GoalUUID&,
                                          std::shared_ptr<const MoveTCP::Goal> goal)
  {
    if (!goal) return rclcpp_action::GoalResponse::REJECT;
    const auto& frame = goal->pick_pose.header.frame_id;
    RCLCPP_INFO(node_->get_logger(), "Received MoveTCP goal (frame=%s)", frame.c_str());
    if (frame.empty()) return rclcpp_action::GoalResponse::REJECT;
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse handle_cancel(const std::shared_ptr<GoalHandleMoveTCP>)
  {
    RCLCPP_WARN(node_->get_logger(), "Cancel requested — stopping motion.");
    move_group_->stop();
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void handle_accepted(const std::shared_ptr<GoalHandleMoveTCP> gh)
  {
    std::thread{std::bind(&ArmController::execute, this, gh)}.detach();
  }

  // ---------------- Execute one goal (approach -> descend), OMPL only ----------------
  void execute(const std::shared_ptr<GoalHandleMoveTCP> gh)
  {
    const auto goal = gh->get_goal();
    auto feedback = std::make_shared<MoveTCP::Feedback>();
    auto result   = std::make_shared<MoveTCP::Result>();

    // 1) Pose → planning frame
    geometry_msgs::msg::PoseStamped target = goal->pick_pose;
    const std::string planning_frame = move_group_->getPlanningFrame();
    if (target.header.frame_id != planning_frame) {
      try {
        auto tf_stamped = tf_buffer_.lookupTransform(planning_frame, target.header.frame_id, tf2::TimePointZero);
        geometry_msgs::msg::PoseStamped converted;
        tf2::doTransform(target, converted, tf_stamped);
        target = converted;
      } catch (tf2::TransformException& ex) {
        RCLCPP_ERROR(node_->get_logger(), "TF failed: %s", ex.what());
        result->success = false; result->message = "tf failed";
        gh->abort(result); return;
      }
    }

    // 2) Force tool-down (roll=0, pitch=pi, yaw keep 0 to standardize)
    {
      tf2::Quaternion q; q.setRPY(0.0, M_PI, 0.0);
      q.normalize();
      target.pose.orientation = tf2::toMsg(q);
    }

    // 3) Build constraints (tool-down, yaw free)
    moveit_msgs::msg::Constraints cstr = orientation_down_constraint();

    // 4) Split: approach 10 cm above, then descend
    const auto current_pose = move_group_->getCurrentPose().pose;
    geometry_msgs::msg::Pose lift = current_pose;
    lift.position.z += 0.15;

    geometry_msgs::msg::Pose approach = target.pose;
    approach.position.z += 0.15;

    
    feedback->stage = "planning_lift"; feedback->progress_percent = 60.0f; gh->publish_feedback(feedback);
    bool ok = plan_and_execute_to_pose(lift, cstr, "lift");
    

    if (ok) {
      feedback->stage = "planning_approach"; feedback->progress_percent = 10.0f; gh->publish_feedback(feedback);
      ok = plan_and_execute_to_pose(approach, cstr, "approach");
    }

    if (ok) {
      feedback->stage = "planning_descend"; feedback->progress_percent = 60.0f; gh->publish_feedback(feedback);
      ok = plan_and_execute_to_pose(target.pose, cstr, "descend");
    }

    if (ok) {
      feedback->stage = "done"; feedback->progress_percent = 100.0f; gh->publish_feedback(feedback);
      result->success = true; result->message = "OK";
      gh->succeed(result);
    } else {
      result->success = false; result->message = "planning/exec failed";
      gh->abort(result);
    }
  }

  // ---------------- One plan+execute to a constrained pose ----------------
  bool plan_and_execute_to_pose(const geometry_msgs::msg::Pose& goal_pose,
                              const moveit_msgs::msg::Constraints& cstr,
                              const std::string& tag)
{
  move_group_->stop();
  move_group_->clearPoseTargets();
  move_group_->clearPathConstraints();

  const auto current_pose = move_group_->getCurrentPose().pose;
  const double dx = goal_pose.position.x - current_pose.position.x;
  const double dy = goal_pose.position.y - current_pose.position.y;
  const double dz = goal_pose.position.z - current_pose.position.z;
  const double distance = std::sqrt(dx*dx + dy*dy + dz*dz);

  RCLCPP_INFO(node_->get_logger(), "[%s] distance = %.3f m", tag.c_str(), distance);

  bool success = false;

  // --- 1) Short motion → Cartesian path ---
  if (distance < 0.60)
  {
    RCLCPP_INFO(node_->get_logger(), "[%s] Using Cartesian planner", tag.c_str());
    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(goal_pose);

    moveit_msgs::msg::RobotTrajectory trajectory;
    const double eef_step = 0.001;  // 1 mm resolution
    const double jump_threshold = 0.0;
    double fraction = move_group_->computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);

    if (fraction > 0.5)
    {
      moveit::planning_interface::MoveGroupInterface::Plan plan;
      plan.trajectory_ = trajectory;
      // RCLCPP_INFO("Cartesian Path planned");
      success = (move_group_->execute(plan) == moveit::core::MoveItErrorCode::SUCCESS);
      
    }
    else
    {
      RCLCPP_WARN(node_->get_logger(), "[%s] Cartesian path incomplete (%.1f%%)", tag.c_str(), fraction * 100.0);
      success = false;
    }
  }
  // --- 2) Longer motion → OMPL planner ---
  else
  {
    RCLCPP_INFO(node_->get_logger(), "[%s] Using OMPL planner", tag.c_str());
    move_group_->setPathConstraints(cstr);
    move_group_->setPoseTarget(goal_pose);

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    auto code = move_group_->plan(plan);
    if (code == moveit::core::MoveItErrorCode::SUCCESS &&
        !plan.trajectory_.joint_trajectory.points.empty())
    {
      success = (move_group_->execute(plan) == moveit::core::MoveItErrorCode::SUCCESS);
    }
    move_group_->clearPathConstraints();
  }

  if (!success)
    RCLCPP_ERROR(node_->get_logger(), "[%s] Motion failed.", tag.c_str());
  else
    RCLCPP_INFO(node_->get_logger(), "[%s] Motion complete.", tag.c_str());

  return success;
}


  // ---------------- Constraints & scene (mirrors the “working” server) ----------------
  moveit_msgs::msg::Constraints orientation_down_constraint()
  {
    moveit_msgs::msg::Constraints constraints;
    moveit_msgs::msg::OrientationConstraint ocm;

    ocm.link_name = move_group_->getEndEffectorLink();
    ocm.header.frame_id = move_group_->getPlanningFrame();
    ocm.absolute_x_axis_tolerance = 0.01;  // tight roll
    ocm.absolute_y_axis_tolerance = 0.01;  // tight pitch
    ocm.absolute_z_axis_tolerance = 3.14159; // yaw free
    ocm.weight = 1.0;

    tf2::Quaternion q; q.setRPY(0, M_PI, 0);
    ocm.orientation = tf2::toMsg(q);

    constraints.orientation_constraints.push_back(ocm);
    return constraints;
  }

  // void setupJointConstraint

  void setupCollisionObjects()
  {
    const std::string frame_id = "world"; // match your working server
    moveit::planning_interface::PlanningSceneInterface psi;

    psi.applyCollisionObject(generateBox(2.4, 0.04, 3.0, 0.70, -0.60, 0.5,  frame_id, "backWall"));
    psi.applyCollisionObject(generateBox(0.04, 2.4, 3.0, -0.55, 0.25, 0.8,  frame_id, "sideWall"));
    psi.applyCollisionObject(generateBox(3.0, 3.0, 0.01, 0.85, 0.25, 0.05,  frame_id, "table"));
    psi.applyCollisionObject(generateBox(2.4, 2.4, 0.04, 0.85, 0.25, 1.5,  frame_id, "ceiling"));
  }

  moveit_msgs::msg::CollisionObject generateBox(float sx,float sy,float sz,
                                                float x,float y,float z,
                                                const std::string& frame_id,
                                                const std::string& id)
  {
    moveit_msgs::msg::CollisionObject co;
    co.header.frame_id = frame_id;
    co.id = id;

    shape_msgs::msg::SolidPrimitive prim;
    prim.type = prim.BOX;
    prim.dimensions = {sx, sy, sz};

    geometry_msgs::msg::Pose p;
    p.orientation.w = 1.0;
    p.position.x = x; p.position.y = y; p.position.z = z;

    co.primitives.push_back(prim);
    co.primitive_poses.push_back(p);
    co.operation = co.ADD;
    return co;
  }

private:
  rclcpp::Node::SharedPtr node_;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  tf2_ros::Buffer tf_buffer_;
  tf2_ros::TransformListener tf_listener_;
  rclcpp_action::Server<MoveTCP>::SharedPtr action_server_;
};

// ---------------- main: same pattern as the working server ----------------
int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>("arm_controller_node");
  ArmController controller(node);
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
