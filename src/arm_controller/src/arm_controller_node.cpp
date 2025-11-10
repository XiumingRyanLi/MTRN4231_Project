#include <memory>
#include <thread>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <geometry_msgs/msg/pose.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/collision_object.hpp>
#include <moveit_msgs/msg/orientation_constraint.hpp>
#include <moveit_msgs/msg/constraints.hpp>
#include <moveit_msgs/msg/position_constraint.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>

#include "custom_interfaces/action/move_tcp.hpp"

using MoveTCP = custom_interfaces::action::MoveTCP;
using GoalHandleMoveTCP = rclcpp_action::ServerGoalHandle<MoveTCP>;

class ArmControllerNode : public rclcpp::Node
{
public:
  ArmControllerNode()
  : Node("arm_controller_node",
         rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true)),
    move_group_interface_(std::shared_ptr<rclcpp::Node>(this, [](auto*){}), "ur_manipulator"),
    tf_buffer_(this->get_clock()),
    tf_listener_(tf_buffer_)
  {
    // Action server: use YOUR action and server name
    action_server_ = rclcpp_action::create_server<MoveTCP>(
        this,
        "arm/pick_place",
        std::bind(&ArmControllerNode::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
        std::bind(&ArmControllerNode::handle_cancel, this, std::placeholders::_1),
        std::bind(&ArmControllerNode::handle_accepted, this, std::placeholders::_1));

    // MoveIt setup
    // move_group_interface_.setEndEffectorLink("tool0");
    move_group_interface_.setPlanningTime(30.0);
    move_group_interface_.setNumPlanningAttempts(30);
    move_group_interface_.setPlannerId("LBKPIECEkConfigDefault"); // OMPL planner
    move_group_interface_.setMaxVelocityScalingFactor(0.25);
    move_group_interface_.setMaxAccelerationScalingFactor(0.25);

    // Optional: constraints you can apply per-goal
    // (we’ll build them inside execute)
    setupCollisionObjects();

    RCLCPP_INFO(this->get_logger(),
                "ArmControllerNode ready (group=%s, tcp=%s, planner=%s)",
                move_group_interface_.getName().c_str(),
                move_group_interface_.getEndEffectorLink().c_str(),
                move_group_interface_.getPlannerId().c_str());
  }

private:
  // ---------- Action server plumbing ----------
  rclcpp_action::GoalResponse handle_goal(
      const rclcpp_action::GoalUUID&,
      std::shared_ptr<const MoveTCP::Goal> goal)
  {
    const auto frame = goal ? goal->pick_pose.header.frame_id : std::string{};
    RCLCPP_INFO(this->get_logger(), "Received MoveTCP goal (frame=%s)", frame.c_str());
    if (!goal || frame.empty()) return rclcpp_action::GoalResponse::REJECT;
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse handle_cancel(const std::shared_ptr<GoalHandleMoveTCP>)
  {
    RCLCPP_INFO(this->get_logger(), "Canceling current goal");
    move_group_interface_.stop();
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void handle_accepted(const std::shared_ptr<GoalHandleMoveTCP> goal_handle)
  {
    std::thread{std::bind(&ArmControllerNode::execute, this, goal_handle)}.detach();
  }

  // ---------- Execute one goal (plan -> execute with OMPL) ----------
  void execute(const std::shared_ptr<GoalHandleMoveTCP> goal_handle)
  {
    const auto goal = goal_handle->get_goal();

    // 1) Resolve target pose (your action carries PoseStamped: pick_pose)
    geometry_msgs::msg::PoseStamped pick_in_base = goal->pick_pose;
    if (pick_in_base.header.frame_id.empty())
    {
      RCLCPP_ERROR(this->get_logger(), "Empty frame_id in goal.");
      auto res = std::make_shared<MoveTCP::Result>(); res->success = false; res->message = "empty frame";
      goal_handle->abort(res); return;
    }

    // Transform to planning frame if needed
    const std::string planning_frame = move_group_interface_.getPlanningFrame();
    if (pick_in_base.header.frame_id != planning_frame)
    {
      try {
        geometry_msgs::msg::TransformStamped tf_stamped =
            tf_buffer_.lookupTransform(planning_frame, pick_in_base.header.frame_id, tf2::TimePointZero);
        geometry_msgs::msg::PoseStamped transformed;
        tf2::doTransform(pick_in_base, transformed, tf_stamped);
        pick_in_base = transformed;
      } catch (tf2::TransformException& ex) {
        RCLCPP_ERROR(this->get_logger(), "TF transform failed: %s", ex.what());
        auto res = std::make_shared<MoveTCP::Result>(); res->success = false; res->message = "tf failed";
        goal_handle->abort(res); return;
      }
    }

    // 2) Force tool-down (roll=pi, optional yaw free)
    {
      tf2::Quaternion q_src; tf2::fromMsg(pick_in_base.pose.orientation, q_src);
      double r, p, y; tf2::Matrix3x3(q_src).getRPY(r, p, y);
      tf2::Quaternion q_down; q_down.setRPY(0.0, M_PI, 0.0); // yaw=0 to standardize
      q_down.normalize();
      pick_in_base.pose.orientation = tf2::toMsg(q_down);
    }

    // 3) Build constraints (orientation + gentle joint bias) like the sample
    moveit_msgs::msg::Constraints constraints = setOrientationDownConstraint();
    constraints.joint_constraints.push_back(createJointConstraint("shoulder_lift_joint", -1.2, 1.0, 1.0, 0.5));
    constraints.joint_constraints.push_back(createJointConstraint("elbow_joint",          1.6,  1.2, 1.2, 0.5));
    constraints.joint_constraints.push_back(createJointConstraint("wrist_2_joint",        1.57, 1.57, 1.57, 0.2));

    // 4) Split into approach and pick (like your original logic but OMPL only)
    geometry_msgs::msg::Pose approach = pick_in_base.pose;
    approach.position.z += 0.10; // approach offset

    bool ok =
      plan_and_execute_to_pose(approach, constraints, "approach") &&
      plan_and_execute_to_pose(pick_in_base.pose, constraints, "descend");

    auto result = std::make_shared<MoveTCP::Result>();
    if (ok) {
      result->success = true;  result->message = "OK";
      goal_handle->succeed(result);
    } else {
      result->success = false; result->message = "planning failed";
      goal_handle->abort(result);
    }
  }

  // ---------- One OMPL plan+execute to a pose with constraints ----------
  bool plan_and_execute_to_pose(const geometry_msgs::msg::Pose& target,
                                const moveit_msgs::msg::Constraints& cstr,
                                const std::string& tag)
  {
    move_group_interface_.stop();
    move_group_interface_.clearPoseTargets();
    move_group_interface_.clearPathConstraints();

    // Apply constraints
    move_group_interface_.setPathConstraints(cstr);
    move_group_interface_.setPoseTarget(target, move_group_interface_.getEndEffectorLink());

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    auto ok = move_group_interface_.plan(plan);
    if (!ok || plan.trajectory_.joint_trajectory.points.size() < 2) {
      RCLCPP_ERROR(this->get_logger(), "[%s] plan failed or too short.", tag.c_str());
      move_group_interface_.clearPathConstraints();
      return false;
    }
    ok = move_group_interface_.execute(plan);
    move_group_interface_.clearPathConstraints();
    if (!ok) {
      RCLCPP_ERROR(this->get_logger(), "[%s] execute failed.", tag.c_str());
      return false;
    }
    return true;
  }

  // ---------- Constraints & scene, matching the sample’s style ----------
  moveit_msgs::msg::Constraints setOrientationDownConstraint()
  {
    moveit_msgs::msg::Constraints constraints;
    moveit_msgs::msg::OrientationConstraint ocm;

    ocm.link_name = move_group_interface_.getEndEffectorLink();
    ocm.header.frame_id = move_group_interface_.getPlanningFrame();
    ocm.absolute_x_axis_tolerance = 0.3;
    ocm.absolute_y_axis_tolerance = 0.3;
    ocm.absolute_z_axis_tolerance = 3.14; // free yaw
    ocm.weight = 1.0;

    tf2::Quaternion q; q.setRPY(0, M_PI, 0); // tool-down
    ocm.orientation = tf2::toMsg(q);

    constraints.orientation_constraints.push_back(ocm);
    return constraints;
  }

  moveit_msgs::msg::JointConstraint createJointConstraint(
      const std::string& joint_name, double position, double tol_above,
      double tol_below, double weight)
  {
    moveit_msgs::msg::JointConstraint jc;
    jc.joint_name = joint_name;
    jc.position = position;
    jc.tolerance_above = tol_above;
    jc.tolerance_below = tol_below;
    jc.weight = weight;
    return jc;
  }

  void setupCollisionObjects()
  {
    moveit::planning_interface::PlanningSceneInterface psi;
    const std::string frame_id = move_group_interface_.getPlanningFrame();

    psi.applyCollisionObject(generateCollisionObject(2.4, 0.04, 1.0, 0.85, -0.30, 0.5, frame_id, "backWall"));
    psi.applyCollisionObject(generateCollisionObject(0.04, 1.2, 1.0, -0.30, 0.25, 0.5, frame_id, "sideWall"));
    psi.applyCollisionObject(generateCollisionObject(2.4, 2.4, 0.01, 0.85, 0.25, 0.013, frame_id, "table"));
    psi.applyCollisionObject(generateCollisionObject(2.4, 2.4, 0.04, 0.85, 0.25, 1.2, frame_id, "ceiling"));
  }

  moveit_msgs::msg::CollisionObject generateCollisionObject(
      float sx, float sy, float sz, float x, float y, float z,
      const std::string& frame_id, const std::string& id)
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

  // ---------- Members (match sample layout) ----------
  moveit::planning_interface::MoveGroupInterface move_group_interface_;
  tf2_ros::Buffer tf_buffer_;
  tf2_ros::TransformListener tf_listener_;
  rclcpp_action::Server<MoveTCP>::SharedPtr action_server_;
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ArmControllerNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
