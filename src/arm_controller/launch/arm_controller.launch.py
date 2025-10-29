from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    planning_group = LaunchConfiguration("planning_group")
    base_frame     = LaunchConfiguration("base_frame")
    tcp_link       = LaunchConfiguration("tcp_link")
    vel_scale      = LaunchConfiguration("vel_scale")
    acc_scale      = LaunchConfiguration("acc_scale")
    approach_dz    = LaunchConfiguration("approach_dz")

    return LaunchDescription([
        DeclareLaunchArgument("planning_group", default_value="manipulator"),
        DeclareLaunchArgument("base_frame",     default_value="base_link"),
        DeclareLaunchArgument("tcp_link",       default_value="tool0"),
        DeclareLaunchArgument("vel_scale",      default_value="0.3"),
        DeclareLaunchArgument("acc_scale",      default_value="0.3"),
        DeclareLaunchArgument("approach_dz",    default_value="0.10"),

        Node(
            package="arm_controller",
            executable="arm_controller_node",
            name="arm_controller",
            output="screen",
            parameters=[{
                "planning_group": planning_group,
                "base_frame":     base_frame,
                "tcp_link":       tcp_link,
                "vel_scale":      vel_scale,
                "acc_scale":      acc_scale,
                "approach_dz":    approach_dz,
            }]
        )
    ])
