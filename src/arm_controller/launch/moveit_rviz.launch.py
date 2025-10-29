from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ur_type      = LaunchConfiguration("ur_type")
    robot_ip     = LaunchConfiguration("robot_ip")
    use_fake_hw  = LaunchConfiguration("use_fake_hardware")
    launch_rviz  = LaunchConfiguration("launch_rviz")
    launch_moveit= LaunchConfiguration("launch_moveit")
    viz_yaml     = LaunchConfiguration("visual_parameters_file")

    return LaunchDescription([
        DeclareLaunchArgument("ur_type", default_value="ur5e"),
        # robot_ip is required by the driver entrypoint; with fake hardware it is ignored
        DeclareLaunchArgument("robot_ip", default_value="192.168.0.100"),
        DeclareLaunchArgument("use_fake_hardware", default_value="true"),
        DeclareLaunchArgument("launch_rviz", default_value="true"),
        DeclareLaunchArgument("launch_moveit", default_value="true"),
        DeclareLaunchArgument(
            "visual_parameters_file",
            default_value="/opt/ros/humble/share/ur_description/config/ur5/visual_parameters.yaml"
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare("ur_robot_driver"),
                    "launch", "ur_control.launch.py"
                ])
            ]),
            launch_arguments={
                "ur_type": ur_type,
                "robot_ip": robot_ip,
                "use_fake_hardware": use_fake_hw,
                "launch_rviz": launch_rviz,
                "launch_moveit": launch_moveit,
                # this flows into ur.urdf.xacro inside the driver
                "visual_parameters_file": viz_yaml,
                # optional toggles you can add:
                # "headless_mode": "false",
                # "initial_joint_controller": "scaled_joint_trajectory_controller",
            }.items()
        ),
    ])
