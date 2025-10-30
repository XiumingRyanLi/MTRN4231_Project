from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    ur_type = LaunchConfiguration("ur_type")
    planning_group = LaunchConfiguration("planning_group")
    base_frame = LaunchConfiguration("base_frame")
    tcp_link = LaunchConfiguration("tcp_link")
    vel_scale = LaunchConfiguration("vel_scale")
    acc_scale = LaunchConfiguration("acc_scale")
    approach_dz = LaunchConfiguration("approach_dz")
    keep_yaw = LaunchConfiguration("keep_yaw")
    use_oc = LaunchConfiguration("use_orientation_constraint")

    return LaunchDescription([
        DeclareLaunchArgument("ur_type", default_value="ur5e"),
        DeclareLaunchArgument("planning_group", default_value="manipulator"),
        DeclareLaunchArgument("base_frame", default_value="base_link"),
        DeclareLaunchArgument("tcp_link", default_value="tool0"),
        DeclareLaunchArgument("vel_scale", default_value="0.3"),
        DeclareLaunchArgument("acc_scale", default_value="0.3"),
        DeclareLaunchArgument("approach_dz", default_value="0.10"),
        DeclareLaunchArgument("keep_yaw", default_value="false"),
        DeclareLaunchArgument("use_orientation_constraint", default_value="true"),

        # Build the same MoveIt config the UR5e uses
        # This injects robot_description, robot_description_semantic, kinematics, OMPL, joint limits, etc.
        # If your SRDF/URDF are custom, change .planning_group to match your file names.
        Node(
            package="arm_controller",
            executable="arm_controller_node",
            name="arm_controller",
            output="screen",
            parameters=[
                # MoveIt parameters
                MoveItConfigsBuilder("ur5e", package_name="ur_moveit_config")
                  .to_moveit_configs()
                  .to_dict(),
                # Your node params
                {
                    "planning_group": planning_group,
                    "base_frame": base_frame,
                    "tcp_link": tcp_link,
                    "vel_scale": vel_scale,
                    "acc_scale": acc_scale,
                    "approach_dz": approach_dz,
                    "keep_yaw": keep_yaw,
                    "use_orientation_constraint": use_oc
                }
            ]
        ),
    ])
