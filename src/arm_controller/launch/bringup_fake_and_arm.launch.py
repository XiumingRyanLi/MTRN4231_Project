from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, TextSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    use_fake     = LaunchConfiguration("use_fake_hardware")
    launch_rviz  = LaunchConfiguration("launch_rviz")
    planning_group = LaunchConfiguration("planning_group")
    base_frame   = LaunchConfiguration("base_frame")
    tcp_link     = LaunchConfiguration("tcp_link")
    vel_scale    = LaunchConfiguration("vel_scale")
    acc_scale    = LaunchConfiguration("acc_scale")
    approach_dz  = LaunchConfiguration("approach_dz")
    keep_yaw     = LaunchConfiguration("keep_yaw")
    use_oc       = LaunchConfiguration("use_orientation_constraint")

    this_pkg = FindPackageShare("arm_controller")
    ur_robot_driver = FindPackageShare("ur_robot_driver")

    # Build URDF via xacro (NO ur_type arg)
    urdf_cmd = Command([
        "xacro ",
        PathJoinSubstitution([this_pkg, "urdf", "ur5e_with_tool.urdf.xacro"]),
        " name:=ur5e",
        " use_fake_hardware:=", use_fake,
        " prefix:=",
        " visual_parameters_file:=",
        TextSubstitution(text="/opt/ros/humble/share/ur_description/config/ur5/visual_parameters.yaml")
    ])

    # SRDF (plain .srdf is okay; run through xacro for consistency)
    srdf_cmd = Command([
        "xacro ",
        PathJoinSubstitution([this_pkg, "srdf", "ur5e_with_tool.srdf"])
    ])

    return LaunchDescription([
        DeclareLaunchArgument("use_fake_hardware", default_value="true"),
        DeclareLaunchArgument("launch_rviz", default_value="true"),
        DeclareLaunchArgument("planning_group", default_value="manipulator"),
        DeclareLaunchArgument("base_frame", default_value="base_link"),
        # if you want to plan to the TCP alias we added in URDF, set default to "tcp_link"
        DeclareLaunchArgument("tcp_link", default_value="tool0"),
        DeclareLaunchArgument("vel_scale", default_value="0.3"),
        DeclareLaunchArgument("acc_scale", default_value="0.3"),
        DeclareLaunchArgument("approach_dz", default_value="0.10"),
        DeclareLaunchArgument("keep_yaw", default_value="false"),
        DeclareLaunchArgument("use_orientation_constraint", default_value="true"),

        # UR bringup (fake) + MoveIt + RViz
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([ur_robot_driver, "launch", "ur_control.launch.py"])
            ),
            launch_arguments={
                "ur_type": TextSubstitution(text="ur5e"),
                "robot_ip": TextSubstitution(text="192.168.0.100"),  # ignored in fake
                "use_fake_hardware": use_fake,
                "launch_moveit": TextSubstitution(text="true"),
                "launch_rviz": launch_rviz,
                "visual_parameters_file": TextSubstitution(
                    text="/opt/ros/humble/share/ur_description/config/ur5/visual_parameters.yaml"
                ),
            }.items()
        ),

        # Your controller, with matching robot_description(+_semantic)
        Node(
            package="arm_controller",
            executable="arm_controller_node",
            name="arm_controller",
            output="screen",
            parameters=[
                {"robot_description":          ParameterValue(urdf_cmd, value_type=str)},
                {"robot_description_semantic": ParameterValue(srdf_cmd, value_type=str)},
                {
                    "planning_group": planning_group,
                    "base_frame":     base_frame,
                    "tcp_link":       tcp_link,
                    "vel_scale":      vel_scale,
                    "acc_scale":      acc_scale,
                    "approach_dz":    approach_dz,
                    "keep_yaw":       keep_yaw,
                    "use_orientation_constraint": use_oc,
                }
            ]
        ),
    ])
