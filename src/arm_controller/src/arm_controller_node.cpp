#include <memory>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <cmath>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/pose.hpp>

#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>

#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/orientation_constraint.hpp>
#include <moveit_msgs/msg/constraints.hpp>
#include <moveit_msgs/msg/robot_trajectory.hpp>

#include <custom_interfaces/action/move_tcp.hpp>

using namespace std::chrono_literals;
namespace rca = rclcpp_action;

class ArmController : public rclcpp::Node
{
public:
  using MoveTCP = custom_interfaces::action::MoveTCP;
  using GoalHandle = rca::ServerGoalHandle<MoveTCP>;

  ArmController()
  : rclcpp::Node("arm_controller")
  {
    // ---------- Parameters ----------
    planning_group_  = this->declare_parameter<std::string>("planning_group", "ur_manipulator");
    base_frame_      = this->declare_parameter<std::string>("base_frame", "base_link");
    tcp_link_        = this->declare_parameter<std::string>("tcp_link", "tool0");

    vel_scale_       = this->declare_parameter<double>("vel_scale", 0.2);
    acc_scale_       = this->declare_parameter<double>("acc_scale", 0.2);
    approach_dz_     = this->declare_parameter<double>("approach_dz", 0.08);

    keep_yaw_        = this->declare_parameter<bool>("keep_yaw", false);
    use_path_constraint_ = this->declare_parameter<bool>("use_orientation_constraint", false);
    tol_x_           = this->declare_parameter<double>("oc_tol_x", 0.15);
    tol_y_           = this->declare_parameter<double>("oc_tol_y", 0.15);
    tol_z_           = this->declare_parameter<double>("oc_tol_z", 0.50);
    oc_weight_       = this->declare_parameter<double>("oc_weight", 1.0);

    planner_id_      = this->declare_parameter<std::string>("planner_id", "RRTConnectkConfigDefault");
    planning_time_   = this->declare_parameter<double>("planning_time", 5.0);
    retries_         = this->declare_parameter<int>("plan_retries", 3);
    execute_         = this->declare_parameter<bool>("execute", false);

    // ---------- TF ----------
    tf_buffer_   = std::make_shared<tf2_ros::Buffer>(this->get_clock());
    tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

    // ---------- Defer MoveIt init (avoid bad_weak_ptr) ----------
    init_timer_ = this->create_wall_timer(
      500ms,  // slight delay so node is fully managed by shared_ptr
      std::bind(&ArmController::init_moveit, this)
    );

    RCLCPP_INFO(get_logger(), "Starting ArmController — waiting for MoveIt initialization...");
  }

private:
  // ===================== Deferred initialization =====================
  void init_moveit()
  {
    if (initialized_) return;
    try {
      // Now shared_from_this() is valid
      move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
        this->shared_from_this(), planning_group_);

      move_group_->setPlanningPipelineId("ompl");
      move_group_->setPlannerId(planner_id_);
      move_group_->setPlanningTime(planning_time_);
      move_group_->setMaxVelocityScalingFactor(vel_scale_);
      move_group_->setMaxAccelerationScalingFactor(acc_scale_);
      move_group_->setGoalPositionTolerance(0.01);
      move_group_->setGoalOrientationTolerance(0.05);

      // Create action server only after MoveIt is ready
      action_server_ = rca::create_server<MoveTCP>(
        this,
        "arm/pick_place",
        std::bind(&ArmController::handle_goal,    this, std::placeholders::_1, std::placeholders::_2),
        std::bind(&ArmController::handle_cancel,  this, std::placeholders::_1),
        std::bind(&ArmController::handle_accepted,this, std::placeholders::_1));

      initialized_ = true;
      init_timer_->cancel();

      RCLCPP_INFO(get_logger(),
        "ArmController ready — action /arm/pick_place, group=%s, tcp=%s, base=%s",
        planning_group_.c_str(), tcp_link_.c_str(), base_frame_.c_str());
    }
    catch (const std::exception& e) {
      RCLCPP_WARN(get_logger(), "MoveIt init not ready yet (%s); retrying...", e.what());
      // keep timer alive to retry
    }
  }

  // ========================== ACTION HANDLERS =========================
  rca::GoalResponse handle_goal(const rclcpp_action::GoalUUID&,
                                std::shared_ptr<const MoveTCP::Goal> goal)
  {
    if (!initialized_) {
      RCLCPP_ERROR(get_logger(), "Rejecting goal: controller not initialized yet.");
      return rca::GoalResponse::REJECT;
    }
    if (!goal || goal->pick_pose.header.frame_id.empty()) {
      RCLCPP_ERROR(get_logger(), "Rejecting goal: pick_pose.header.frame_id is empty.");
      return rca::GoalResponse::REJECT;
    }
    return rca::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rca::CancelResponse handle_cancel(const std::shared_ptr<GoalHandle>)
  {
    if (move_group_) move_group_->stop();
    return rca::CancelResponse::ACCEPT;
  }

  void handle_accepted(const std::shared_ptr<GoalHandle> gh)
  {
    std::thread{std::bind(&ArmController::execute, this, gh)}.detach();
  }

  // ============================ EXECUTION =============================
  void execute(const std::shared_ptr<GoalHandle> gh)
  {
    auto result = std::make_shared<MoveTCP::Result>();
    if (!initialized_ || !move_group_) {
      result->success = false;
      result->message = "Not initialized";
      gh->abort(result);
      return;
    }

    const auto goal = gh->get_goal();

    // Transform goal to base frame
    geometry_msgs::msg::PoseStamped pick_in_base;
    if (!transform_to_base(goal->pick_pose, pick_in_base)) {
      return fail(gh, result, "transform_to_base");
    }

    // Force Z-down (optionally keep yaw)
    pick_in_base.pose.orientation = tf2::toMsg(make_down_quat(pick_in_base.pose.orientation, keep_yaw_));

    // Stage 1: approach
    geometry_msgs::msg::PoseStamped approach = pick_in_base;
    approach.pose.position.z += approach_dz_;

    publish_feedback(gh, "approach_pick", 0.0);
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    if (!tryPlanPose(approach, plan)) {
      // Tight? Try smaller dz
      approach.pose.position.z = pick_in_base.pose.position.z + std::max(0.03, approach_dz_ * 0.5);
      if (!tryPlanPose(approach, plan)) return fail(gh, result, "approach_pick");
    }
    if (!maybe_execute(plan, "approach_pick")) return fail(gh, result, "approach_pick");
    publish_feedback(gh, "approach_pick", 33.0);

    // Stage 2: descend
    publish_feedback(gh, "descend_to_pick", 33.0);
    if (!tryPlanPose(pick_in_base, plan)) return fail(gh, result, "descend_to_pick");
    if (!maybe_execute(plan, "descend_to_pick")) return fail(gh, result, "descend_to_pick");
    publish_feedback(gh, "descend_to_pick", 66.0);

    // Stage 3: retreat
    publish_feedback(gh, "retreat", 66.0);
    geometry_msgs::msg::PoseStamped retreat = pick_in_base;
    retreat.pose.position.z += approach_dz_;
    if (!tryPlanPose(retreat, plan)) return fail(gh, result, "retreat");
    if (!maybe_execute(plan, "retreat")) return fail(gh, result, "retreat");
    publish_feedback(gh, "retreat", 100.0);

    result->success = true;
    result->message = "OK";
    gh->succeed(result);
  }

  // ========================== PLANNING HELPERS ========================
  void prepForPlanning()
  {
    move_group_->stop();
    move_group_->clearPoseTargets();
    move_group_->clearPathConstraints();
    move_group_->setStartStateToCurrentState();
    move_group_->setPlannerId(planner_id_);
    move_group_->setPlanningTime(planning_time_);
    move_group_->setMaxVelocityScalingFactor(vel_scale_);
    move_group_->setMaxAccelerationScalingFactor(acc_scale_);
  }

  moveit_msgs::msg::Constraints makeZDownConstraint(double tx, double ty, double tz, double weight)
  {
    moveit_msgs::msg::Constraints c;
    moveit_msgs::msg::OrientationConstraint oc;
    oc.header.frame_id = base_frame_;
    oc.link_name = tcp_link_;
    tf2::Quaternion q; q.setRPY(0.0, M_PI, 0.0);  // Z-down
    oc.orientation = tf2::toMsg(q);
    oc.absolute_x_axis_tolerance = tx;
    oc.absolute_y_axis_tolerance = ty;
    oc.absolute_z_axis_tolerance = tz;
    oc.weight = weight;
    c.orientation_constraints.push_back(oc);
    return c;
  }

  bool tryPlanPose(const geometry_msgs::msg::PoseStamped& target,
                   moveit::planning_interface::MoveGroupInterface::Plan& plan)
  {
    static const char* kPlanners[] = {
      "RRTConnectkConfigDefault",
      "RRTstarkConfigDefault",
      "PRMkConfigDefault"
    };

    // Attempt 1: (optional) path constraint with retries
    for (int r = 0; r < std::max(1, retries_); ++r) {
      for (auto pid : kPlanners) {
        prepForPlanning();
        move_group_->setPlannerId(pid);
        move_group_->setPoseTarget(target, tcp_link_);
        if (use_path_constraint_) {
          move_group_->setPathConstraints(makeZDownConstraint(tol_x_, tol_y_, tol_z_, oc_weight_));
        }
        if (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS) return true;
      }
    }

    // Attempt 2: relaxed constraint
    for (auto pid : kPlanners) {
      prepForPlanning();
      move_group_->setPlannerId(pid);
      move_group_->setPoseTarget(target, tcp_link_);
      if (use_path_constraint_) {
        move_group_->setPathConstraints(makeZDownConstraint(
          std::max(0.30, tol_x_), std::max(0.30, tol_y_), std::max(0.80, tol_z_), 0.2));
      }
      if (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS) return true;
    }

    // Attempt 3: no path constraint
    prepForPlanning();
    move_group_->setPoseTarget(target, tcp_link_);
    if (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS) return true;

    // Attempt 4: short Cartesian segment to the target
    prepForPlanning();
    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(target.pose);
    moveit_msgs::msg::RobotTrajectory traj;
    double frac = move_group_->computeCartesianPath(waypoints, 0.01, 0.0, traj, true);
    if (frac > 0.95) {
      plan.trajectory_ = traj;
      plan.planning_time_ = 0.0;
      return true;
    }
    return false;
  }

  bool maybe_execute(const moveit::planning_interface::MoveGroupInterface::Plan& plan,
                     const std::string& stage)
  {
    if (!execute_) {
      RCLCPP_INFO(get_logger(), "[%s] Planned (execute:=false).", stage.c_str());
      return true;
    }
    auto exec = move_group_->execute(plan);
    if (exec != moveit::core::MoveItErrorCode::SUCCESS) {
      RCLCPP_ERROR(get_logger(), "Execution failed at: %s", stage.c_str());
      return false;
    }
    return true;
  }

  // ============================== UTIL ===============================
  tf2::Quaternion make_down_quat(const geometry_msgs::msg::Quaternion& q_in, bool keep_yaw) const
  {
    tf2::Quaternion q; tf2::fromMsg(q_in, q);
    double roll, pitch, yaw; tf2::Matrix3x3(q).getRPY(roll, pitch, yaw);
    if (!keep_yaw) yaw = 0.0;
    tf2::Quaternion q_down; q_down.setRPY(0.0, M_PI, yaw);
    q_down.normalize();
    return q_down;
  }

  bool transform_to_base(const geometry_msgs::msg::PoseStamped& in,
                         geometry_msgs::msg::PoseStamped& out)
  {
    try {
      if (in.header.frame_id == base_frame_) {
        out = in;
        return true;
      }
      geometry_msgs::msg::TransformStamped tf =
        tf_buffer_->lookupTransform(base_frame_, in.header.frame_id, tf2::TimePointZero);
      tf2::doTransform(in, out, tf);
      return true;
    } catch (const tf2::TransformException& ex) {
      RCLCPP_ERROR(get_logger(), "TF transform failed: %s", ex.what());
      return false;
    }
  }

  void publish_feedback(const std::shared_ptr<GoalHandle>& gh,
                        const std::string& stage, double percent)
  {
    auto fb = std::make_shared<MoveTCP::Feedback>();
    fb->stage = stage;
    fb->progress_percent = percent;
    gh->publish_feedback(fb);
  }

  void fail(const std::shared_ptr<GoalHandle>& gh,
            const std::shared_ptr<MoveTCP::Result>& res,
            const std::string& where)
  {
    res->success = false;
    res->message = "Failed at stage: " + where;
    gh->abort(res);
  }

private:
  // Params
  std::string planning_group_, base_frame_, tcp_link_, planner_id_;
  double vel_scale_{0.2}, acc_scale_{0.2}, approach_dz_{0.08};
  bool keep_yaw_{false}, use_path_constraint_{false}, execute_{false};
  double tol_x_{0.15}, tol_y_{0.15}, tol_z_{0.50}, oc_weight_{1.0};
  double planning_time_{5.0};
  int retries_{3};

  // MoveIt
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  moveit::planning_interface::PlanningSceneInterface psi_;

  // Action server
  rca::Server<MoveTCP>::SharedPtr action_server_;

  // TF
  std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;

  // Init
  rclcpp::TimerBase::SharedPtr init_timer_;
  bool initialized_{false};
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ArmController>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
