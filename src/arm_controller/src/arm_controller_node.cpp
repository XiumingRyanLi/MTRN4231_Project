#include <memory>
#include <thread>
#include <string>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>

#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

#include "custom_interfaces/action/move_tcp.hpp"
#include "custom_interfaces/action/gripper_command.hpp"

using custom_interfaces::action::MoveTCP;
namespace rca = rclcpp_action;

class ArmController : public rclcpp::Node {
public:
  using GoalHandle = rca::ServerGoalHandle<MoveTCP>;

  ArmController()
  : rclcpp::Node("arm_controller")
  {
    // ---- Parameters
    planning_group_ = this->declare_parameter<std::string>("planning_group", "manipulator");
    base_frame_     = this->declare_parameter<std::string>("base_frame",     "base_link");
    tcp_link_       = this->declare_parameter<std::string>("tcp_link",       "tool0");
    vel_scale_      = this->declare_parameter<double>("vel_scale",           0.2);
    acc_scale_      = this->declare_parameter<double>("acc_scale",           0.2);
    approach_dz_    = this->declare_parameter<double>("approach_dz",         0.10);
    planner_id_     = this->declare_parameter<std::string>("planner_id",     "");

    // ---- TF: construct AFTER node exists; use shared_ptrs
    tf_buffer_   = std::make_shared<tf2_ros::Buffer>(this->get_clock());
    tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

    // ---- MoveIt interface
    move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
      shared_from_this(), planning_group_);
    move_group_->setPoseReferenceFrame(base_frame_);
    move_group_->setEndEffectorLink(tcp_link_);
    move_group_->setMaxVelocityScalingFactor(vel_scale_);
    move_group_->setMaxAccelerationScalingFactor(acc_scale_);
    if (!planner_id_.empty()) move_group_->setPlannerId(planner_id_);

    // ---- Action server
    action_server_ = rca::create_server<MoveTCP>(
      this,
      "arm/pick_place",
      std::bind(&ArmController::handle_goal,     this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&ArmController::handle_cancel,   this, std::placeholders::_1),
      std::bind(&ArmController::handle_accepted, this, std::placeholders::_1)
    );

    RCLCPP_INFO(get_logger(), "ArmController ready — action: /arm/pick_place, group=%s, tcp=%s, base=%s",
                planning_group_.c_str(), tcp_link_.c_str(), base_frame_.c_str());
  }

private:
  // ===== Action callbacks =====
  rca::GoalResponse handle_goal(const rclcpp_action::GoalUUID&,
                                std::shared_ptr<const MoveTCP::Goal> /*goal*/) {
    return rca::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rca::CancelResponse handle_cancel(const std::shared_ptr<GoalHandle> /*gh*/) {
    move_group_->stop();
    RCLCPP_WARN(get_logger(), "Goal cancelled; stopping MoveIt.");
    return rca::CancelResponse::ACCEPT;
  }

  void handle_accepted(const std::shared_ptr<GoalHandle> gh) {
    std::thread([this, gh]() { execute(gh); }).detach();
  }

  // ===== Execution =====
  void execute(std::shared_ptr<GoalHandle> gh) {
    const auto goal = gh->get_goal();
    auto result = std::make_shared<MoveTCP::Result>();

    geometry_msgs::msg::PoseStamped pick_in_base;
    if (!transform_to_base(goal->pick_pose, pick_in_base)) {
      result->success = false;
      result->message = "TF transform to base_frame failed";
      gh->abort(result);
      return;
    }

    geometry_msgs::msg::Pose approach = pick_in_base.pose;
    approach.position.z += approach_dz_;

    if (!plan_and_execute(approach, "approach_pick", gh)) { fail(gh, result, "approach_pick"); return; }
    if (!plan_and_execute(pick_in_base.pose, "grasp", gh)) { fail(gh, result, "grasp"); return; }

    geometry_msgs::msg::Pose lift = approach;
    if (!plan_and_execute(lift, "lift", gh)) { fail(gh, result, "lift"); return; }

    result->success = true;
    result->message = "Reached pick pose (approach, descend, lift complete)";
    gh->succeed(result);
  }

  bool plan_and_execute(const geometry_msgs::msg::Pose& target_pose,
                        const std::string& stage,
                        const std::shared_ptr<GoalHandle>& gh) {
    publish_feedback(gh, stage, 0.0);

    move_group_->setPoseTarget(target_pose, tcp_link_);
    moveit::planning_interface::MoveGroupInterface::Plan plan;

    bool planned = (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS);
    if (!planned) { RCLCPP_ERROR(get_logger(), "Planning failed at: %s", stage.c_str()); return false; }

    auto exec = move_group_->execute(plan);
    if (exec != moveit::core::MoveItErrorCode::SUCCESS) {
      RCLCPP_ERROR(get_logger(), "Execution failed at: %s", stage.c_str()); return false;
    }

    publish_feedback(gh, stage, 100.0);
    return true;
  }

  void publish_feedback(const std::shared_ptr<GoalHandle>& gh,
                        const std::string& stage,
                        double percent) {
    auto fb = std::make_shared<MoveTCP::Feedback>();
    fb->stage = stage;
    fb->progress_percent = percent;
    gh->publish_feedback(fb);
  }

  void fail(std::shared_ptr<GoalHandle> gh,
            std::shared_ptr<MoveTCP::Result> res,
            const std::string& where) {
    res->success = false;
    res->message = "Failed at stage: " + where;
    gh->abort(res);
  }

  bool transform_to_base(const geometry_msgs::msg::PoseStamped& in,
                         geometry_msgs::msg::PoseStamped& out) {
    if (in.header.frame_id.empty() || in.header.frame_id == base_frame_) {
      out = in;
      out.header.frame_id = base_frame_;
      if (out.header.stamp.sec == 0 && out.header.stamp.nanosec == 0) out.header.stamp = now();
      return true;
    }
    try {
      out = tf_buffer_->transform(in, base_frame_, tf2::durationFromSec(0.2));
      return true;
    } catch (const tf2::TransformException& ex) {
      RCLCPP_ERROR(get_logger(), "TF transform error: %s", ex.what());
      return false;
    }
  }

  // ===== Members =====
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  std::string planning_group_, base_frame_, tcp_link_, planner_id_;
  double vel_scale_{0.2}, acc_scale_{0.2}, approach_dz_{0.1};

  rca::Server<MoveTCP>::SharedPtr action_server_;
  std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ArmController>());
  rclcpp::shutdown();
  return 0;
}
