#include <memory>
#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <arm_interfaces/action/pick_place.hpp>

using arm_interfaces::action::PickPlace;
namespace rca = rclcpp_action;

class ArmController : public rclcpp::Node {
public:
  using GoalHandle = rca::ServerGoalHandle<PickPlace>;

  ArmController() : Node("arm_controller") {
    planning_group_ = this->declare_parameter<std::string>("planning_group", "manipulator");
    base_frame_     = this->declare_parameter<std::string>("base_frame",     "base_link");
    tcp_link_       = this->declare_parameter<std::string>("tcp_link",       "tool0");
    vel_scale_      = this->declare_parameter<double>("vel_scale", 0.2);
    acc_scale_      = this->declare_parameter<double>("acc_scale", 0.2);

    move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(shared_from_this(), planning_group_);
    move_group_->setPoseReferenceFrame(base_frame_);
    move_group_->setEndEffectorLink(tcp_link_);
    move_group_->setMaxVelocityScalingFactor(vel_scale_);
    move_group_->setMaxAccelerationScalingFactor(acc_scale_);

    action_server_ = rca::create_server<PickPlace>(
      this,
      "arm/pick_place",
      std::bind(&ArmController::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&ArmController::handle_cancel, this, std::placeholders::_1),
      std::bind(&ArmController::handle_accepted, this, std::placeholders::_1)
    );

    RCLCPP_INFO(get_logger(), "ArmController action server ready on /arm/pick_place");
  }

private:
  rca::GoalResponse handle_goal(const rclcpp_action::GoalUUID&,
                                std::shared_ptr<const PickPlace::Goal> goal) {
    if (goal->lift_distance <= 0.0) {
      RCLCPP_WARN(get_logger(), "lift_distance must be > 0");
      return rca::GoalResponse::REJECT;
    }
    return rca::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rca::CancelResponse handle_cancel(const std::shared_ptr<GoalHandle>) {
    move_group_->stop();
    return rca::CancelResponse::ACCEPT;
  }

  void handle_accepted(const std::shared_ptr<GoalHandle> gh) {
    std::thread([this, gh]() { execute(gh); }).detach();
  }

  bool linear_step(const geometry_msgs::msg::Pose& target, const std::string& stage,
                   std::shared_ptr<GoalHandle> gh) {
    auto fb = std::make_shared<PickPlace::Feedback>();
    fb->stage = stage;
    fb->progress_percent = 0.0;
    gh->publish_feedback(fb);

    move_group_->setPoseTarget(target, tcp_link_);
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    if (!move_group_->plan(plan)) {
    RCLCPP_ERROR(get_logger(), "Planning failed at stage: %s", stage.c_str());
    return false;
    }

    auto ec = move_group_->execute(plan);
    if (!ec) {
    RCLCPP_ERROR(get_logger(), "Execution failed at stage: %s", stage.c_str());
    return false;
    }

    fb->progress_percent = 100.0;
    gh->publish_feedback(fb);
    return true;
  }

  void execute(std::shared_ptr<GoalHandle> gh) {
    const auto goal = gh->get_goal();
    auto result = std::make_shared<PickPlace::Result>();

    auto pick = goal->pick_pose;   // already at grasp height
    auto place = goal->place_pose; // already at release height
    double dz = goal->lift_distance;

    // Build approach/retreat poses in base frame (assumes +Z is "up")
    auto up = [](const geometry_msgs::msg::Pose& p, double dz){
      auto q = p; q.position.z += dz; return q;
    };
    auto pick_above  = up(pick.pose, dz);
    auto place_above = up(place.pose, dz);

    // 1) Approach pick (above -> down)
    if (!linear_step(pick_above,  "approach_pick", gh)) { fail(gh, result, "approach_pick"); return; }
    if (!linear_step(pick.pose,   "descend_pick",  gh)) { fail(gh, result, "descend_pick");  return; }

    // 2) Close gripper (replace with your real gripper call)
    publish_stage(gh, "grasp", 50.0);
    // TODO: call your gripper service/action here

    // 3) Lift
    if (!linear_step(pick_above,  "lift",          gh)) { fail(gh, result, "lift");          return; }

    // 4) Transfer (above pick -> above place)
    if (!linear_step(place_above, "transfer",      gh)) { fail(gh, result, "transfer");      return; }

    // 5) Lower to place
    if (!linear_step(place.pose,  "lower_place",   gh)) { fail(gh, result, "lower_place");   return; }

    // 6) Open gripper
    publish_stage(gh, "release", 80.0);
    // TODO: open gripper

    // 7) Retreat up
    if (!linear_step(place_above, "retreat",       gh)) { fail(gh, result, "retreat");       return; }

    result->success = true;
    result->message = "PickPlace complete";
    gh->succeed(result);
  }

  void publish_stage(std::shared_ptr<GoalHandle> gh, const std::string& s, double pct) {
    auto fb = std::make_shared<PickPlace::Feedback>();
    fb->stage = s;
    fb->progress_percent = pct;
    gh->publish_feedback(fb);
  }

  void fail(std::shared_ptr<GoalHandle> gh, std::shared_ptr<PickPlace::Result> res, const std::string& where) {
    res->success = false;
    res->message = "Failed at " + where;
    gh->abort(res);
  }

  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  std::string planning_group_, base_frame_, tcp_link_;
  double vel_scale_{0.2}, acc_scale_{0.2};
  rca::Server<PickPlace>::SharedPtr action_server_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ArmController>());
  rclcpp::shutdown();
  return 0;
}
