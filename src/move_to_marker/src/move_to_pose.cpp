#include <memory>
#include <string>
#include <vector>
#include <chrono>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/collision_object.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>

using namespace std::chrono_literals;

static moveit_msgs::msg::CollisionObject makeBox(
  const std::string& id, const std::string& frame,
  double sx, double sy, double sz,
  double cx, double cy, double cz)
{
  moveit_msgs::msg::CollisionObject co;
  co.id = id;
  co.header.frame_id = frame;

  shape_msgs::msg::SolidPrimitive prim;
  prim.type = shape_msgs::msg::SolidPrimitive::BOX;
  prim.dimensions = {sx, sy, sz};

  geometry_msgs::msg::Pose pose;
  pose.orientation.w = 1.0;  // axis-aligned
  pose.position.x = cx;
  pose.position.y = cy;
  pose.position.z = cz;

  co.primitives.push_back(prim);
  co.primitive_poses.push_back(pose);
  co.operation = co.ADD;
  return co;
}

class MoveToPoseNode : public rclcpp::Node {
public:
  MoveToPoseNode() : Node("move_to_pose")
  {
    // ---- Parameters
    this->declare_parameter<std::string>("group_name", "ur_manipulator");
    this->declare_parameter<std::string>("base_frame", "base_link");
    this->declare_parameter<bool>("execute", true);
    this->declare_parameter<double>("planning_time", 5.0);

    // ---- Defer MoveIt init to avoid std::bad_weak_ptr
    init_timer_ = this->create_wall_timer(
      100ms, std::bind(&MoveToPoseNode::init_moveit, this));

    // ---- Subscribe for target poses (PoseStamped in base_frame)
    sub_ = this->create_subscription<geometry_msgs::msg::PoseStamped>(
      "/target_pose", 10,
      std::bind(&MoveToPoseNode::on_target_pose, this, std::placeholders::_1));
  }

private:
  void init_moveit()
  {
    if (move_group_) return;

    const auto group_name = this->get_parameter("group_name").as_string();
    const auto base_frame = this->get_parameter("base_frame").as_string();
    const auto plan_time  = this->get_parameter("planning_time").as_double();

    // Create MoveGroupInterface AFTER node is fully constructed
    move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
        shared_from_this(), group_name);

    move_group_->setPlanningTime(plan_time);
    move_group_->setPoseReferenceFrame(base_frame);

    planning_frame_ = move_group_->getPlanningFrame();
    RCLCPP_INFO(this->get_logger(), "MoveIt ready. Planning frame: %s, EE: %s",
                planning_frame_.c_str(), move_group_->getEndEffectorLink().c_str());

    // Add safety geometry once
    if (!collision_applied_) {
      std::vector<moveit_msgs::msg::CollisionObject> objs;
      // Tune these for your cell (units: meters, frame: planning_frame_)
      objs.push_back(makeBox("backWall", planning_frame_, 2.4, 0.04, 1.8, 0.85, -0.60, 0.90));
      objs.push_back(makeBox("sideWall", planning_frame_, 0.04, 2.4, 1.8, -0.55, 0.25, 0.90));
      objs.push_back(makeBox("table",    planning_frame_, 2.0,  1.5, 0.05, 0.85,  0.25, 0.03));
      objs.push_back(makeBox("ceiling",  planning_frame_, 2.4,  2.4, 0.04, 0.85,  0.25, 1.60));
      psi_.applyCollisionObjects(objs);
      collision_applied_ = true;
      RCLCPP_INFO(this->get_logger(), "Applied %zu collision objects.", objs.size());
    }

    init_timer_->cancel();
  }

  void on_target_pose(const geometry_msgs::msg::PoseStamped::SharedPtr msg)
  {
    if (!move_group_) {
      RCLCPP_WARN(this->get_logger(), "MoveIt not ready yet. Ignoring target.");
      return;
    }

    const auto base_frame = this->get_parameter("base_frame").as_string();
    if (msg->header.frame_id != base_frame) {
      RCLCPP_ERROR(this->get_logger(),
        "Target frame_id='%s' != base_frame param '%s'. Publish pose in base frame.",
        msg->header.frame_id.c_str(), base_frame.c_str());
      return;
    }

    move_group_->setPoseReferenceFrame(base_frame);
    move_group_->setPoseTarget(*msg);

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    auto result = move_group_->plan(plan);
    if (result != moveit::core::MoveItErrorCode::SUCCESS) {
      RCLCPP_WARN(this->get_logger(), "Planning failed.");
      return;
    }

    if (this->get_parameter("execute").as_bool()) {
      auto exec_ok = (move_group_->execute(plan) == moveit::core::MoveItErrorCode::SUCCESS);
      if (!exec_ok) {
        RCLCPP_ERROR(this->get_logger(), "Execution failed (no controller or controller error).");
        return;
      }
      RCLCPP_INFO(this->get_logger(), "Motion complete.");
    } else {
      RCLCPP_INFO(this->get_logger(), "Plan computed (execute:=false).");
    }
  }

private:
  // Timers
  rclcpp::TimerBase::SharedPtr init_timer_;

  // MoveIt
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  moveit::planning_interface::PlanningSceneInterface psi_;
  std::string planning_frame_;
  bool collision_applied_{false};

  // ROS
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr sub_;
};

int main(int argc, char* argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MoveToPoseNode>());
  rclcpp::shutdown();
  return 0;
}
