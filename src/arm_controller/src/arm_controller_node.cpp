#include <memory>
#include <string>
#include <thread>
#include <vector>
#include <chrono>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <geometry_msgs/msg/transform_stamped.hpp>

#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>

#include <shape_msgs/msg/solid_primitive.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/constraints.hpp>
#include <moveit_msgs/msg/orientation_constraint.hpp>
#include <moveit_msgs/msg/position_constraint.hpp>
#include <moveit_msgs/msg/robot_trajectory.hpp>

#include <moveit_visual_tools/moveit_visual_tools.h>
#include <Eigen/Core>

#include "custom_interfaces/action/move_tcp.hpp"

using custom_interfaces::action::MoveTCP;
namespace rca = rclcpp_action;
namespace rvt = rviz_visual_tools;
using namespace std::chrono_literals;

class ArmController : public rclcpp::Node {
public:
  using GoalHandle = rca::ServerGoalHandle<MoveTCP>;

  ArmController() : rclcpp::Node("arm_controller") {
    // ---- Parameters (safe in ctor) ------------------------------------------
    planning_group_ = declare_parameter<std::string>("planning_group", "ur_manipulator");
    base_frame_     = declare_parameter<std::string>("base_frame",     "base_link");
    tcp_link_       = declare_parameter<std::string>("tcp_link",       "tool0");

    vel_scale_      = declare_parameter<double>("vel_scale",           0.20);
    acc_scale_      = declare_parameter<double>("acc_scale",           0.20);
    planning_time_  = declare_parameter<double>("planning_time",       10.0);
    planner_id_     = declare_parameter<std::string>("planner_id",     "RRTConnectkConfigDefault");

    approach_dz_    = declare_parameter<double>("approach_dz",         0.08);
    keep_yaw_       = declare_parameter<bool>("keep_yaw",              false);
    execute_        = declare_parameter<bool>("execute",               true);

    // Orientation path constraint (Z-down)
    use_orientation_constraint_ = declare_parameter<bool>("use_orientation_constraint", true);
    oc_tol_x_     = declare_parameter<double>("oc_tol_x",   1.0);
    oc_tol_y_     = declare_parameter<double>("oc_tol_y",   1.0);
    oc_tol_z_     = declare_parameter<double>("oc_tol_z",   1.0);
    oc_weight_    = declare_parameter<double>("oc_weight",  0.1);

    // Box position constraint + visual
    enable_box_constraint_ = declare_parameter<bool>("enable_box_constraint", true);
    box_size_x_ = declare_parameter<double>("box_size_x", 0.40);
    box_size_y_ = declare_parameter<double>("box_size_y", 0.80);
    box_size_z_ = declare_parameter<double>("box_size_z", 0.70);
    box_center_y_ = declare_parameter<double>("box_center_y", 0.45);
    box_center_z_ = declare_parameter<double>("box_center_z", 0.45);
    box_weight_   = declare_parameter<double>("box_weight",   1.0);

    retries_ = declare_parameter<int>("plan_retries", 2);

    // ---- Defer everything that needs shared_from_this() ----------------------
    init_timer_ = create_wall_timer(200ms, [this] {
      if (initialized_) return;
      try { late_init(); initialized_ = true; init_timer_->cancel(); }
      catch (const std::exception& e) {
        RCLCPP_WARN(get_logger(), "MoveIt init retry: %s", e.what());
      }
    });
  }

private:
  // -------- util requested by you: collision object generator ----------------
  moveit_msgs::msg::CollisionObject generateCollisionObject(
      float sx, float sy, float sz, float x, float y, float z,
      const std::string& frame_id, const std::string& id) {
    moveit_msgs::msg::CollisionObject collision_object;
    collision_object.header.frame_id = frame_id;
    collision_object.id = id;

    shape_msgs::msg::SolidPrimitive primitive;
    primitive.type = primitive.BOX;
    primitive.dimensions.resize(3);
    primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_X] = sx;
    primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_Y] = sy;
    primitive.dimensions[shape_msgs::msg::SolidPrimitive::BOX_Z] = sz;

    geometry_msgs::msg::Pose box_pose;
    box_pose.orientation.w = 1.0;
    box_pose.position.x = x;
    box_pose.position.y = y;
    box_pose.position.z = z;

    collision_object.primitives.push_back(primitive);
    collision_object.primitive_poses.push_back(box_pose);
    collision_object.operation = collision_object.ADD;
    return collision_object;
  }

  // --------------------------- deferred init ---------------------------------
  void late_init() {
    auto node = shared_from_this();

    // TF
    tf_buffer_   = std::make_shared<tf2_ros::Buffer>(get_clock());
    tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

    // MoveIt interfaces
    move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(node, planning_group_);
    move_group_->setPoseReferenceFrame(base_frame_);
    move_group_->setEndEffectorLink(tcp_link_);
    move_group_->setPlanningTime(planning_time_);
    move_group_->setPlannerId(planner_id_);
    move_group_->setMaxVelocityScalingFactor(vel_scale_);
    move_group_->setMaxAccelerationScalingFactor(acc_scale_);
    move_group_->setGoalPositionTolerance(0.01);
    move_group_->setGoalOrientationTolerance(0.05);

    planning_scene_interface_ = std::make_shared<moveit::planning_interface::PlanningSceneInterface>();

    // Visual tools
    moveit_visual_tools_ = std::make_shared<moveit_visual_tools::MoveItVisualTools>(
      node, base_frame_, rvt::RVIZ_MARKER_TOPIC, move_group_->getRobotModel());
    moveit_visual_tools_->deleteAllMarkers();
    moveit_visual_tools_->loadRemoteControl();
    moveit_visual_tools_->trigger();

    // Seed static scene (table/walls/box demo)
    seed_environment();

    // Action server
    action_server_ = rca::create_server<MoveTCP>(
      node,
      "arm/pick_place",
      std::bind(&ArmController::handle_goal,     this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&ArmController::handle_cancel,   this, std::placeholders::_1),
      std::bind(&ArmController::handle_accepted, this, std::placeholders::_1));

    RCLCPP_INFO(get_logger(),
      "ArmController ready — /arm/pick_place, group=%s, tcp=%s, base=%s",
      planning_group_.c_str(), tcp_link_.c_str(), base_frame_.c_str());
  }

  void seed_environment() {
    const std::string frame_id = move_group_->getPlanningFrame();

    // your requested objects:
    auto collision_object     = generateCollisionObject(0.08f, 0.6f, 0.57f, 0.5f, 0.2f, 0.2f, frame_id, "box");
    auto col_object_table     = generateCollisionObject(2.4f, 1.2f, 0.04f, 0.85f, 0.25f, -0.03f, frame_id, "table");
    auto col_object_backWall  = generateCollisionObject(2.4f, 0.04f, 1.0f, 0.85f, -0.45f, 0.5f, frame_id, "backWall");
    auto col_object_sideWall  = generateCollisionObject(0.04f, 1.2f, 1.0f, -0.45f, 0.25f, 0.5f, frame_id, "sideWall");

    std::vector<moveit_msgs::msg::CollisionObject> objs;
    objs.push_back(col_object_table);
    objs.push_back(col_object_backWall);
    objs.push_back(col_object_sideWall);
    // (optional) objs.push_back(collision_object);

    planning_scene_interface_->applyCollisionObjects(objs);
  }

  // --------------------------- action plumbing -------------------------------
  rca::GoalResponse handle_goal(const rclcpp_action::GoalUUID&,
                                std::shared_ptr<const MoveTCP::Goal> goal) {
    if (!goal || goal->pick_pose.header.frame_id.empty())
      return rca::GoalResponse::REJECT;
    return rca::GoalResponse::ACCEPT_AND_EXECUTE;
  }
  rca::CancelResponse handle_cancel(const std::shared_ptr<GoalHandle>) {
    if (move_group_) move_group_->stop();
    return rca::CancelResponse::ACCEPT;
  }
  void handle_accepted(const std::shared_ptr<GoalHandle> gh) {
    std::thread([this, gh]() { execute(gh); }).detach();
  }

  // ------------------------------ execute ------------------------------------
  void execute(const std::shared_ptr<GoalHandle>& gh) {
    auto result = std::make_shared<MoveTCP::Result>();
    if (!move_group_) { result->success=false; result->message="MoveGroup not ready"; gh->abort(result); return; }

    // Transform goal to base frame
    geometry_msgs::msg::PoseStamped pick_in_base;
    if (!transform_to_base(gh->get_goal()->pick_pose, pick_in_base)) {
      result->success = false; result->message = "TF transform failed"; gh->abort(result); return;
    }

    // Force Z-down orientation (optionally keep yaw)
    pick_in_base.pose.orientation = tf2::toMsg(make_down_quat(pick_in_base.pose.orientation, keep_yaw_));

    // Build + apply constraints (box + orientation), and visualize the box
    if (enable_box_constraint_) {
      apply_and_visualize_box_constraint(pick_in_base.pose.position.x);
    } else {
      move_group_->clearPathConstraints();
    }
    if (use_orientation_constraint_) {
      auto c = create_path_constraints();
      // merge (box constraint may already be set)
      auto existing = move_group_->getPathConstraints();
      existing.orientation_constraints.insert(existing.orientation_constraints.end(),
                                              c.orientation_constraints.begin(),
                                              c.orientation_constraints.end());
      move_group_->setPathConstraints(existing);
    }

    // Stages: approach -> descend -> retreat
    geometry_msgs::msg::Pose approach = pick_in_base.pose;
    approach.position.z += approach_dz_;

    if (!plan_with_fallbacks(approach, "approach_pick", gh)) { return fail(gh, result, "approach_pick"); }
    if (!plan_with_fallbacks(pick_in_base.pose, "descend_to_pick", gh)) { return fail(gh, result, "descend_to_pick"); }

    geometry_msgs::msg::Pose retreat = pick_in_base.pose;
    retreat.position.z += approach_dz_;
    if (!plan_with_fallbacks(retreat, "retreat", gh)) { return fail(gh, result, "retreat"); }

    // clear visuals after success
    if (moveit_visual_tools_) { moveit_visual_tools_->deleteAllMarkers(); moveit_visual_tools_->trigger(); }
    move_group_->clearPathConstraints();

    result->success = true; result->message = "OK";
    gh->succeed(result);
  }

  // ------------------------- constraints & visuals ---------------------------
  moveit_msgs::msg::Constraints create_path_constraints() {
    moveit_msgs::msg::Constraints constraints;

    moveit_msgs::msg::OrientationConstraint oc;
    oc.header.frame_id = move_group_->getPlanningFrame();
    oc.link_name       = move_group_->getEndEffectorLink();
    tf2::Quaternion q; q.setRPY(0, M_PI, 0); // Z-down
    oc.orientation = tf2::toMsg(q);
    oc.absolute_x_axis_tolerance = oc_tol_x_;
    oc.absolute_y_axis_tolerance = oc_tol_y_;
    oc.absolute_z_axis_tolerance = oc_tol_z_;
    oc.weight = oc_weight_;

    constraints.orientation_constraints.push_back(oc);
    return constraints;
  }

  void apply_and_visualize_box_constraint(double center_x) {
    // Build box primitive for constraint
    shape_msgs::msg::SolidPrimitive box;
    box.type = shape_msgs::msg::SolidPrimitive::BOX;
    box.dimensions = { box_size_x_, box_size_y_, box_size_z_ };

    geometry_msgs::msg::Pose box_pose;
    box_pose.orientation.w = 1.0;
    box_pose.position.x = center_x;
    box_pose.position.y = box_center_y_;
    box_pose.position.z = box_center_z_;

    // Visualize the cuboid in RViz
    if (moveit_visual_tools_) {
      Eigen::Vector3d p1(
        box_pose.position.x - box.dimensions[0] / 2.0,
        box_pose.position.y - box.dimensions[1] / 2.0,
        box_pose.position.z - box.dimensions[2] / 2.0);
      Eigen::Vector3d p2(
        box_pose.position.x + box.dimensions[0] / 2.0,
        box_pose.position.y + box.dimensions[1] / 2.0,
        box_pose.position.z + box.dimensions[2] / 2.0);
      moveit_visual_tools_->publishCuboid(p1, p2, rvt::TRANSLUCENT_DARK);
      moveit_visual_tools_->trigger();
    }

    // Apply as path PositionConstraint on TCP
    moveit_msgs::msg::PositionConstraint pc;
    pc.header.frame_id = base_frame_;
    pc.link_name       = tcp_link_;
    pc.constraint_region.primitives.emplace_back(box);
    pc.constraint_region.primitive_poses.emplace_back(box_pose);
    pc.weight = box_weight_;

    moveit_msgs::msg::Constraints cons = move_group_->getPathConstraints();
    cons.position_constraints.clear();
    cons.position_constraints.emplace_back(pc);
    move_group_->setPathConstraints(cons);
  }

  // --------------------------- planning wrappers -----------------------------
  void prep_planning() {
    move_group_->stop();
    move_group_->clearPoseTargets();
    move_group_->setStartStateToCurrentState();
    move_group_->setPlanningTime(planning_time_);
    move_group_->setMaxVelocityScalingFactor(vel_scale_);
    move_group_->setMaxAccelerationScalingFactor(acc_scale_);
    move_group_->setPlannerId(planner_id_);
  }

  bool plan_with_fallbacks(const geometry_msgs::msg::Pose& target,
                           const std::string& stage,
                           const std::shared_ptr<GoalHandle>& gh)
  {
    publish_feedback(gh, stage, 0.0);
    moveit::planning_interface::MoveGroupInterface::Plan plan;

    // Try with current constraints, with small retries
    for (int a = 0; a < std::max(1, retries_); ++a) {
      prep_planning();
      move_group_->setPoseTarget(target, tcp_link_);
      if (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS)
        return maybe_execute(plan, stage);
    }

    // Last resort: tiny Cartesian hop to target pose
    {
      prep_planning();
      std::vector<geometry_msgs::msg::Pose> waypoints{ target };
      moveit_msgs::msg::RobotTrajectory traj;
      double frac = move_group_->computeCartesianPath(waypoints, 0.01, 0.0, traj, true);
      if (frac > 0.95) {
        plan.trajectory_ = traj;
        return maybe_execute(plan, stage);
      }
    }

    RCLCPP_ERROR(get_logger(), "Planning failed at: %s", stage.c_str());
    return false;
  }

  bool maybe_execute(const moveit::planning_interface::MoveGroupInterface::Plan& plan,
                     const std::string& stage)
  {
    if (!execute_) {
      RCLCPP_INFO(get_logger(), "[%s] Planned (execute:=false).", stage.c_str());
      return true;
    }
    auto ok = move_group_->execute(plan);
    if (ok != moveit::core::MoveItErrorCode::SUCCESS) {
      RCLCPP_ERROR(get_logger(), "Execution failed at: %s", stage.c_str());
      return false;
    }
    return true;
  }

  // ------------------------------- helpers -----------------------------------
  tf2::Quaternion make_down_quat(const geometry_msgs::msg::Quaternion& src, bool keep_yaw) {
    tf2::Quaternion q_src; tf2::fromMsg(src, q_src);
    double r, p, y; tf2::Matrix3x3(q_src).getRPY(r, p, y);
    if (!keep_yaw) y = 0.0;
    tf2::Quaternion q_down; q_down.setRPY(0.0, M_PI, y);
    q_down.normalize();
    return q_down;
  }

  bool transform_to_base(const geometry_msgs::msg::PoseStamped& in,
                         geometry_msgs::msg::PoseStamped& out) {
    if (in.header.frame_id.empty() || in.header.frame_id == base_frame_) {
      out = in; out.header.frame_id = base_frame_;
      if (out.header.stamp.sec == 0 && out.header.stamp.nanosec == 0) out.header.stamp = now();
      return true;
    }
    try {
      geometry_msgs::msg::TransformStamped tf =
        tf_buffer_->lookupTransform(base_frame_, in.header.frame_id, tf2::TimePointZero);
      tf2::doTransform(in, out, tf);
      return true;
    } catch (const tf2::TransformException& ex) {
      RCLCPP_ERROR(get_logger(), "TF error: %s", ex.what());
      return false;
    }
  }

  void publish_feedback(const std::shared_ptr<GoalHandle>& gh,
                        const std::string& stage, double percent) {
    auto fb = std::make_shared<MoveTCP::Feedback>();
    fb->stage = stage;
    fb->progress_percent = percent;
    gh->publish_feedback(fb);
  }

  void fail(const std::shared_ptr<GoalHandle>& gh,
            const std::shared_ptr<MoveTCP::Result>& res,
            const std::string& where) {
    res->success = false;
    res->message = "Failed at stage: " + where;
    gh->abort(res);
  }

  // ------------------------------- members -----------------------------------
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  std::shared_ptr<moveit::planning_interface::PlanningSceneInterface> planning_scene_interface_;

  std::shared_ptr<moveit_visual_tools::MoveItVisualTools> moveit_visual_tools_;

  std::string planning_group_, base_frame_, tcp_link_, planner_id_;
  double vel_scale_{0.2}, acc_scale_{0.2}, planning_time_{10.0};
  double approach_dz_{0.08};
  bool keep_yaw_{false};
  bool execute_{true};
  int  retries_{2};

  // constraints
  bool use_orientation_constraint_{true};
  bool enable_box_constraint_{true};
  double oc_tol_x_{1.0}, oc_tol_y_{1.0}, oc_tol_z_{1.0}, oc_weight_{0.1};
  double box_size_x_{0.40}, box_size_y_{0.80}, box_size_z_{0.70};
  double box_center_y_{0.45}, box_center_z_{0.45}, box_weight_{1.0};

  // infra
  rca::Server<MoveTCP>::SharedPtr action_server_;
  std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
  rclcpp::TimerBase::SharedPtr init_timer_;
  bool initialized_{false};
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ArmController>());
  rclcpp::shutdown();
  return 0;
}
