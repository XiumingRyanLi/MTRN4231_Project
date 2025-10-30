from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, TextSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ur_type      = LaunchConfiguration("ur_type")
    robot_ip     = LaunchConfiguration("robot_ip")
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

    this_pkg   = FindPackageShare("arm_controller")
    ur_desc    = FindPackageShare("ur_description")

    # Build robot_description from YOUR xacro (with UR inside)
    urdf_cmd = Command([
        "xacro ",
        PathJoinSubstitution([this_pkg, "urdf", "ur5e_with_tool.urdf.xacro"]),
        " name:=ur5e",
        " ur_type:=", ur_type,
        " use_fake_hardware:=", use_fake,
        " prefix:=",
        " visual_parameters_file:=",
        TextSubstitution(text="/opt/ros/humble/share/ur_description/config/ur5/visual_parameters.yaml")
    ])

    # Build robot_description_semantic from YOUR SRDF (plain SRDF; no xacro expansion needed)
    srdf_path = PathJoinSubstitution([this_pkg, "srdf", "ur5e_with_tool.srdf"])

    return LaunchDescription([
        # ---- args ----
        DeclareLaunchArgument("ur_type", default_value="ur5e"),
        DeclareLaunchArgument("robot_ip", default_value="192.168.0.100"),
        DeclareLaunchArgument("use_fake_hardware", default_value="true"),
        DeclareLaunchArgument("launch_rviz", default_value="true"),
        DeclareLaunchArgument("planning_group", default_value="manipulator"),
        DeclareLaunchArgument("base_frame", default_value="base_link"),
        DeclareLaunchArgument("tcp_link", default_value="tool0"),   # or "tcp_link" if you want the alias above
        DeclareLaunchArgument("vel_scale", default_value="0.3"),
        DeclareLaunchArgument("acc_scale", default_value="0.3"),
        DeclareLaunchArgument("approach_dz", default_value="0.10"),
        DeclareLaunchArgument("keep_yaw", default_value="false"),
        DeclareLaunchArgument("use_orientation_constraint", default_value="true"),

        # Bring up UR stack (fake hardware) + move_group + RViz
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([FindPackageShare("ur_robot_driver"), "launch", "ur_control.launch.py"])
            ),
            launch_arguments={
                "ur_type": ur_type,
                "robot_ip": robot_ip,
                "use_fake_hardware": use_fake,
                "launch_rviz": launch_rviz,
                "launch_moveit": TextSubstitution(text="true"),
                # meshes shading etc.
                "visual_parameters_file": TextSubstitution(
                    text="/opt/ros/humble/share/ur_description/config/ur5/visual_parameters.yaml"
                ),
            }.items()
        ),

        # Start your controller with matching model params
        Node(
            package="arm_controller",
            executable="arm_controller_node",
            name="arm_controller",
            output="screen",
            parameters=[
                {"robot_description": urdf_cmd},
                {"robot_description_semantic": Command(["xacro ", srdf_path])},  # if it's plain .srdf, xacro will just pass it through
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
