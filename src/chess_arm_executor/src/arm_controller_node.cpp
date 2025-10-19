#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include "chess_arm_executor/action/execute_move.hpp"
#include <rcl_interfaces/srv/get_parameters.hpp>

using ExecuteMove = chess_arm_executor::action::ExecuteMove;
using GoalHandle  = rclcpp_action::ServerGoalHandle<ExecuteMove>;

class ChessArmExecutor : public rclcpp::Node {
public:
  ChessArmExecutor() : Node("chess_arm_executor")
  {
    RCLCPP_INFO(get_logger(), "Starting Chess Arm Executor...");

    // Create action server
    action_server_ = rclcpp_action::create_server<ExecuteMove>(
      this, "play_move",
      std::bind(&ChessArmExecutor::handleGoal, this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&ChessArmExecutor::handleCancel, this, std::placeholders::_1),
      std::bind(&ChessArmExecutor::handleAccepted, this, std::placeholders::_1));

     move_group_params_client_ =
    this->create_client<rcl_interfaces::srv::GetParameters>("/move_group/get_parameters");

    // Safe deferred MoveIt initialization
    init_timer_ = this->create_wall_timer(
      std::chrono::milliseconds(100),
      std::bind(&ChessArmExecutor::tryInitMoveGroup, this));
  }

private:
  void tryInitMoveGroup()
  {
    if (move_group_) return;

    // Create the parameter client once
    if (!move_group_params_client_) {
      move_group_params_client_ =
        this->create_client<rcl_interfaces::srv::GetParameters>("/move_group/get_parameters");
    }

    if (!move_group_params_client_->service_is_ready()) {
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 3000,
                          "Waiting for /move_group/get_parameters service...");
      return;
    }

    auto req = std::make_shared<rcl_interfaces::srv::GetParameters::Request>();
    req->names = {
      "robot_description",
      "robot_description_semantic",
      "robot_description_kinematics"  // (json/yaml map; optional but nice to have)
    };

    // Async request; DON'T spin the node (avoids “already added to an executor”)
    move_group_params_client_->async_send_request(
      req,
      [this](rclcpp::Client<rcl_interfaces::srv::GetParameters>::SharedFuture f) {
        const auto resp = f.get();
        if (resp->values.size() < 2) {
          RCLCPP_WARN(get_logger(), "move_group replied without robot descriptions, retrying...");
          return;
        }

        const auto &urdf  = resp->values[0].string_value; // robot_description
        const auto &srdf  = resp->values[1].string_value; // robot_description_semantic
        const auto &kin   = (resp->values.size() > 2) ? resp->values[2].string_value : std::string();

        if (urdf.empty() || srdf.empty()) {
          RCLCPP_WARN(get_logger(), "robot_description/SRDF empty, retrying...");
          return;
        }

        // Mirror the params locally so MoveGroupInterface can find them on THIS node
        // (Nodes must declare before set, unless you enabled undeclared params)
        try {
          if (!this->has_parameter("robot_description"))
            this->declare_parameter<std::string>("robot_description", urdf);
          else
            this->set_parameter(rclcpp::Parameter("robot_description", urdf));

          if (!this->has_parameter("robot_description_semantic"))
            this->declare_parameter<std::string>("robot_description_semantic", srdf);
          else
            this->set_parameter(rclcpp::Parameter("robot_description_semantic", srdf));

          if (!kin.empty()) {
            if (!this->has_parameter("robot_description_kinematics"))
              this->declare_parameter<std::string>("robot_description_kinematics", kin);
            else
              this->set_parameter(rclcpp::Parameter("robot_description_kinematics", kin));
          }
        } catch (const std::exception &e) {
          RCLCPP_ERROR(get_logger(), "Failed declaring/setting robot_description params: %s", e.what());
          return;
        }

        // Now it's safe to construct MoveGroupInterface — it will find the params locally.
        try {
          // Use the same ctor style you liked in moveit_path_planning_server
          move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
            this->shared_from_this(),
            "ur_manipulator",
            std::shared_ptr<tf2_ros::Buffer>(),                 // optional
            rclcpp::Duration::from_seconds(5.0)                 // wait for TF timeout
          );

          move_group_->setPlannerId("RRTConnectkConfigDefault");
          move_group_->setMaxVelocityScalingFactor(0.5);
          move_group_->setMaxAccelerationScalingFactor(0.5);

          RCLCPP_INFO(get_logger(), "MoveIt MoveGroup ready ✅");
          init_timer_->cancel();
        } catch (const std::exception &e) {
          RCLCPP_ERROR(get_logger(), "MoveGroupInterface construction failed: %s", e.what());
        }
      }
    );
  }



  rclcpp_action::GoalResponse handleGoal(
    const rclcpp_action::GoalUUID&,
    std::shared_ptr<const ExecuteMove::Goal> goal)
  {
    if (!move_group_) {
      RCLCPP_WARN(get_logger(), "MoveIt not ready yet.");
      return rclcpp_action::GoalResponse::REJECT;
    }
    if (goal->mode != ExecuteMove::Goal::GO_HOME &&
        goal->mode != ExecuteMove::Goal::MOVE)
      return rclcpp_action::GoalResponse::REJECT;
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse handleCancel(const std::shared_ptr<GoalHandle>)
  {
    if (move_group_) move_group_->stop();
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void handleAccepted(const std::shared_ptr<GoalHandle> goal_handle)
  {
    std::thread([this, goal_handle]() { execute(goal_handle); }).detach();
  }

  void execute(const std::shared_ptr<GoalHandle> gh)
  {
    auto result = std::make_shared<ExecuteMove::Result>();
    const auto goal = gh->get_goal();

    if (!move_group_) {
      result->ok = false;
      result->message = "MoveIt not ready";
      gh->abort(result);
      return;
    }

    if (goal->mode == ExecuteMove::Goal::GO_HOME) {
      move_group_->setNamedTarget("home");
    } else {
      // --- Compute target pose ---
      auto [x, y] = squareXY(goal->dst_square);
      geometry_msgs::msg::PoseStamped target;
      target.header.frame_id = "board";
      target.pose.position.x = x;
      target.pose.position.y = y;
      target.pose.position.z = zPickFor(goal->piece_type);
      tf2::Quaternion q; q.setRPY(0, M_PI, 0);
      target.pose.orientation = tf2::toMsg(q);
      move_group_->setPoseTarget(target);

    }

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    if (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS &&
        move_group_->execute(plan) == moveit::core::MoveItErrorCode::SUCCESS) {
      result->ok = true;
      result->message = "Execution succeeded.";
      gh->succeed(result);
    } else {
      result->ok = false;
      result->message = "Planning or execution failed.";
      gh->abort(result);
    }
  }

  // --- Helpers ---
  std::pair<double, double> squareXY(const std::string& s)
  {
    int file = std::toupper(s[0]) - 'A';
    int rank = s[1] - '1';
    double size = 0.04;
    return {file * size, rank * size};
  }

  double zPickFor(uint8_t piece_type)
  {
    using G = ExecuteMove::Goal;
    switch (piece_type) {
      case G::PAWN:   return 0.018;
      case G::KNIGHT: return 0.022;
      case G::BISHOP: return 0.022;
      case G::ROOK:   return 0.025;
      case G::QUEEN:  return 0.028;
      case G::KING:   return 0.030;
      default:        return 0.018;
    }
  }

  // --- members ---
  rclcpp::TimerBase::SharedPtr init_timer_;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  rclcpp_action::Server<ExecuteMove>::SharedPtr action_server_;
  rclcpp::Client<rcl_interfaces::srv::GetParameters>::SharedPtr move_group_params_client_;

};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ChessArmExecutor>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}

/*
ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur5e \
  robot_ip:=192.168.0.9 \
  use_fake_hardware:=true \
  headless_mode:=true \
  initial_joint_controller:=scaled_joint_trajectory_controller \
  launch_rviz:=false

*/

// ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e launch_rviz:=true

// ros2 launch chess_arm_executor chess_arm_executor.launch.py


// ros2 action send_goal /play_move chess_arm_executor/action/ExecuteMove \
  "{mode: 1, src_square: 'E2', dst_square: 'E4', piece_type: 1}"

