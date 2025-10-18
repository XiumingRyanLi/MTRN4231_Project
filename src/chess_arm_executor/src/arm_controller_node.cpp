#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <std_srvs/srv/empty.hpp>

#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/collision_object.hpp>
#include <moveit_msgs/msg/orientation_constraint.hpp>
#include <moveit_msgs/msg/constraints.hpp>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>

#include <thread>
#include <cctype>
#include <utility>

#include "chess_arm_executor/action/execute_move.hpp"

using ExecuteMove = chess_arm_executor::action::ExecuteMove;
using GoalHandle  = rclcpp_action::ServerGoalHandle<ExecuteMove>;

class ArmControllerNode : public rclcpp::Node {
public:
  ArmControllerNode() : Node("chess_arm_executor") {
    // ---- Parameters ----
    planning_group_ = declare_parameter<std::string>("planning_group", "ur_manipulator");
    ee_link_        = declare_parameter<std::string>("ee_link", "tool0");
    planner_id_     = declare_parameter<std::string>("planner_id", "RRTConnectkConfigDefault");
    vel_            = declare_parameter<double>("velocity_scaling", 0.5);
    acc_            = declare_parameter<double>("accel_scaling", 0.5);

    board_frame_    = declare_parameter<std::string>("board_frame", "board");
    world_frame_    = declare_parameter<std::string>("world_frame", "world");
    square_size_    = declare_parameter<double>("square_size", 0.040);

    // Absolute Z (meters) in the board frame
    z_approach_     = declare_parameter<double>("z_approach", 0.070);

    // Per-piece absolute pick heights (meters, board frame)
    z_pick_pawn_    = declare_parameter<double>("z_pick_pawn",   0.018);
    z_pick_knight_  = declare_parameter<double>("z_pick_knight", 0.022);
    z_pick_bishop_  = declare_parameter<double>("z_pick_bishop", 0.022);
    z_pick_rook_    = declare_parameter<double>("z_pick_rook",   0.025);
    z_pick_queen_   = declare_parameter<double>("z_pick_queen",  0.028);
    z_pick_king_    = declare_parameter<double>("z_pick_king",   0.030);

    home_name_      = declare_parameter<std::string>("home_named_target", "home");

    // ---- MoveIt setup ----
    move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(shared_from_this(), planning_group_);
    move_group_->setEndEffectorLink(ee_link_);
    move_group_->setPlannerId(planner_id_);
    move_group_->setMaxVelocityScalingFactor(vel_);
    move_group_->setMaxAccelerationScalingFactor(acc_);

    // ---- Collision scene ----
    addCollisionObjects();

    // ---- Action server ----
    action_server_ = rclcpp_action::create_server<ExecuteMove>(
      this,
      "play_move",
      std::bind(&ArmControllerNode::handleGoal, this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&ArmControllerNode::handleCancel, this, std::placeholders::_1),
      std::bind(&ArmControllerNode::handleAccepted, this, std::placeholders::_1));

    // ---- Go home service ----
    home_srv_ = create_service<std_srvs::srv::Empty>(
      "go_home",
      std::bind(&ArmControllerNode::goHomeCb, this, std::placeholders::_1, std::placeholders::_2));

    RCLCPP_INFO(get_logger(), "Arm Controller ready.");
  }

private:
  // ---------- Action plumbing ----------
  rclcpp_action::GoalResponse handleGoal(const rclcpp_action::GoalUUID&,
                                         std::shared_ptr<const ExecuteMove::Goal> goal) {
    if (!validSquare(goal->src_square) || !validSquare(goal->dst_square)) {
      RCLCPP_WARN(get_logger(), "Invalid squares: %s -> %s",
                  goal->src_square.c_str(), goal->dst_square.c_str());
      return rclcpp_action::GoalResponse::REJECT;
    }
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse handleCancel(const std::shared_ptr<GoalHandle>) {
    move_group_->stop();
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void handleAccepted(const std::shared_ptr<GoalHandle> gh) {
    std::thread([this, gh]() { executeMove(gh); }).detach();
  }

  void executeMove(const std::shared_ptr<GoalHandle> gh) {
    const auto goal = gh->get_goal();
    auto feedback = std::make_shared<ExecuteMove::Feedback>();
    auto result   = std::make_shared<ExecuteMove::Result>();

    const double z_used = zPickFor(goal->piece_type);

    // Build poses (absolute Z in board frame, Z-down orientation)
    auto p_app_src = poseAtZ(goal->src_square, z_approach_);
    auto p_src     = poseAtZ(goal->src_square, z_used);
    auto p_app_dst = poseAtZ(goal->dst_square, z_approach_);
    auto p_dst     = poseAtZ(goal->dst_square, z_used);

    // Keep EE Z-down (free yaw)
    moveit_msgs::msg::Constraints zdown = zDownConstraint();
    move_group_->setPathConstraints(zdown);

    // 1) approach src
    feedback->stage = "approach_src"; gh->publish_feedback(feedback);
    if (!planExec(p_app_src)) return abortError(gh, result, "approach_src failed");

    // 2) descend src (ready for external gripper close)
    feedback->stage = "descend_src"; gh->publish_feedback(feedback);
    if (!planExec(p_src)) return abortError(gh, result, "descend_src failed");

    // 3) lift
    feedback->stage = "lift"; gh->publish_feedback(feedback);
    if (!planExec(p_app_src)) return abortError(gh, result, "lift failed");

    // 4) transit (approach dst)
    feedback->stage = "transit"; gh->publish_feedback(feedback);
    if (!planExec(p_app_dst)) return abortError(gh, result, "transit failed");

    // 5) descend dst (ready for external gripper open)
    feedback->stage = "descend_dst"; gh->publish_feedback(feedback);
    if (!planExec(p_dst)) return abortError(gh, result, "descend_dst failed");

    move_group_->clearPathConstraints();

    result->ok = true;
    result->message = "At place height; ready for gripper release.";
    gh->succeed(result);
  }

  void abortError(const std::shared_ptr<GoalHandle> gh,
                  const std::shared_ptr<ExecuteMove::Result>& result,
                  const std::string& msg) {
    move_group_->clearPathConstraints();
    result->ok = false; result->message = msg;
    gh->abort(result);
  }

  // ---------- Geometry / helpers ----------
  bool validSquare(const std::string& s) const {
    if (s.size() != 2) return false;
    char f = std::toupper(static_cast<unsigned char>(s[0]));
    char r = s[1];
    return (f >= 'A' && f <= 'H' && r >= '1' && r <= '8');
  }

  std::pair<double,double> squareXY(const std::string& s) const {
    int file = std::toupper(static_cast<unsigned char>(s[0])) - 'A'; // 0..7
    int rank = static_cast<int>(s[1] - '1');                         // 0..7
    return { file * square_size_, rank * square_size_ };
  }

  geometry_msgs::msg::PoseStamped poseAtZ(const std::string& sq, double z_abs) const {
    geometry_msgs::msg::PoseStamped ps; ps.header.frame_id = board_frame_;
    auto xy = squareXY(sq);
    ps.pose.position.x = xy.first;
    ps.pose.position.y = xy.second;
    ps.pose.position.z = z_abs;

    // Z-down orientation (roll=0, pitch=π, yaw free)
    tf2::Quaternion q; q.setRPY(0.0, 3.141592653589793, 0.0);
    ps.pose.orientation = tf2::toMsg(q);
    return ps;
  }

  moveit_msgs::msg::Constraints zDownConstraint() const {
    moveit_msgs::msg::OrientationConstraint oc;
    oc.link_name = ee_link_;
    oc.header.frame_id = board_frame_;
    tf2::Quaternion q; q.setRPY(0.0, 3.141592653589793, 0.0);
    oc.orientation = tf2::toMsg(q);
    oc.absolute_x_axis_tolerance = 0.1;  // radians
    oc.absolute_y_axis_tolerance = 0.1;
    oc.absolute_z_axis_tolerance = 3.14; // yaw free
    oc.weight = 1.0;

    moveit_msgs::msg::Constraints cs;
    cs.orientation_constraints.push_back(oc);
    return cs;
  }

  bool planExec(const geometry_msgs::msg::PoseStamped& target) {
    move_group_->setPoseTarget(target, ee_link_);
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    if (move_group_->plan(plan) != moveit::core::MoveItErrorCode::SUCCESS) {
      move_group_->clearPoseTargets();
      return false;
    }
    auto ok = (move_group_->execute(plan) == moveit::core::MoveItErrorCode::SUCCESS);
    move_group_->clearPoseTargets();
    return ok;
  }

  // ---------- Collision scene ----------
  void addCollisionObjects() {
    moveit::planning_interface::PlanningSceneInterface psi;

    // Table box in world
    moveit_msgs::msg::CollisionObject table;
    table.header.frame_id = world_frame_;
    table.id = "table";
    shape_msgs::msg::SolidPrimitive p1; p1.type = p1.BOX; p1.dimensions = {1.2, 1.2, 0.02};
    geometry_msgs::msg::Pose pose1; pose1.orientation.w = 1.0;
    pose1.position.x = 0.5; pose1.position.y = 0.0; pose1.position.z = -0.01;
    table.primitives = {p1}; table.primitive_poses = {pose1}; table.operation = table.ADD;

    // Thin board “rim” box in board frame (acts like a low collision frame)
    moveit_msgs::msg::CollisionObject board;
    board.header.frame_id = board_frame_;
    board.id = "board_rim";
    shape_msgs::msg::SolidPrimitive p2; p2.type = p2.BOX;
    double L = 8 * square_size_ + 0.02; // board + ~10 mm rim
    p2.dimensions = {L, L, 0.02};
    geometry_msgs::msg::Pose pose2; pose2.orientation.w = 1.0; pose2.position.z = -0.01;
    board.primitives = {p2}; board.primitive_poses = {pose2}; board.operation = board.ADD;

    psi.applyCollisionObjects({table, board});
  }

  // ---------- Services ----------
  void goHomeCb(const std::shared_ptr<std_srvs::srv::Empty::Request>,
                std::shared_ptr<std_srvs::srv::Empty::Response>) {
    move_group_->setNamedTarget(home_name_);
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    if (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS) {
      move_group_->execute(plan);
      RCLCPP_INFO(get_logger(), "Moved to home.");
    } else {
      RCLCPP_WARN(get_logger(), "Home plan failed.");
    }
  }

  // ---------- Piece → pick height ----------
  double zPickFor(uint8_t piece_type) const {
    using P = chess_arm_executor::action::ExecuteMove_Goal; // generated enum constants
    switch (piece_type) {
      case P::PAWN:   return z_pick_pawn_;
      case P::KNIGHT: return z_pick_knight_;
      case P::BISHOP: return z_pick_bishop_;
      case P::ROOK:   return z_pick_rook_;
      case P::QUEEN:  return z_pick_queen_;
      case P::KING:   return z_pick_king_;
      default:        return z_pick_pawn_;
    }
  }

  // ---------- Members ----------
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  rclcpp_action::Server<ExecuteMove>::SharedPtr action_server_;
  rclcpp::Service<std_srvs::srv::Empty>::SharedPtr home_srv_;

  std::string planning_group_, ee_link_, planner_id_, board_frame_, world_frame_, home_name_;
  double vel_, acc_, square_size_, z_approach_;
  double z_pick_pawn_, z_pick_knight_, z_pick_bishop_, z_pick_rook_, z_pick_queen_, z_pick_king_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ArmControllerNode>());
  rclcpp::shutdown();
  return 0;
}
