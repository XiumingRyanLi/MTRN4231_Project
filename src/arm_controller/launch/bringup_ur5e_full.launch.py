from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, FindExecutable
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    # ---- args ----
    ur_type       = LaunchConfiguration("ur_type")
    robot_ip      = LaunchConfiguration("robot_ip")
    use_fake_hw   = LaunchConfiguration("use_fake_hardware")
    launch_rviz   = LaunchConfiguration("launch_rviz")
    execute_moves = LaunchConfiguration("execute")  # true => execute via controller

    ur_description    = FindPackageShare("ur_description")
    ur_moveit_config  = FindPackageShare("ur_moveit_config")
    ur_robot_driver   = FindPackageShare("ur_robot_driver")

    urdf_xacro = PathJoinSubstitution([ur_description, "urdf", "ur.urdf.xacro"])
    srdf_xacro = PathJoinSubstitution([ur_moveit_config, "srdf", "ur.srdf.xacro"])

    joint_limits_yaml = PathJoinSubstitution([ur_description, "config", "ur5e", "joint_limits.yaml"])
    kin_params_yaml   = PathJoinSubstitution([ur_description, "config", "ur5e", "default_kinematics.yaml"])
    phys_params_yaml  = PathJoinSubstitution([ur_description, "config", "ur5e", "physical_parameters.yaml"])
    vis_params_yaml   = PathJoinSubstitution([ur_description, "config", "ur5e", "visual_parameters.yaml"])

    # Build the exact robot_description MoveIt uses
    robot_description_cmd = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        urdf_xacro, " ",
        "ur_type:=", ur_type, " ",
        "name:=", "ur", " ",
        "prefix:=", '""', " ",
        "safety_limits:=", "true", " ",
        "safety_pos_margin:=", "0.15", " ",
        "safety_k_position:=", "20", " ",
        "joint_limit_params:=", joint_limits_yaml, " ",
        "kinematics_params:=", kin_params_yaml, " ",
        "physical_params:=",  phys_params_yaml, " ",
        "visual_params:=",    vis_params_yaml,
    ])

    robot_semantic_cmd = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        srdf_xacro, " ",
        "name:=", "ur", " ",
        "prefix:=", '""'
    ])

    # MoveIt kinematics (this file is a valid ROS params file with 'robot_description_kinematics')
    kinematics_yaml = PathJoinSubstitution([ur_moveit_config, "config", "kinematics.yaml"])

    # --- UR driver (controllers + TF + joint_states) ---
    driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([ur_robot_driver, "launch", "ur_control.launch.py"])
        ),
        launch_arguments={
            "ur_type": ur_type,
            "robot_ip": robot_ip,
            "use_fake_hardware": use_fake_hw,
            "launch_rviz": "false",
            "initial_joint_controller": "scaled_joint_trajectory_controller",
        }.items(),
    )

    # --- MoveIt (move_group + RViz) ---
    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([ur_moveit_config, "launch", "ur_moveit.launch.py"])
        ),
        launch_arguments={
            "ur_type": ur_type,
            "robot_ip": robot_ip,            # required when use_fake_hardware:=false
            "use_fake_hardware": use_fake_hw,
            "launch_rviz": launch_rviz,
        }.items(),
    )

    # --- Your arm_controller (give it the SAME descriptions + kinematics) ---
    arm_controller = Node(
        package="arm_controller",
        executable="arm_controller_node",
        name="arm_controller",
        output="screen",
        parameters=[
            {"robot_description": robot_description_cmd},
            {"robot_description_semantic": robot_semantic_cmd},
            kinematics_yaml,  # provides 'robot_description_kinematics'
            {
                "planning_group": "manipulator",
                "base_frame": "base_link",
                "tcp_link": "tool0",
                "vel_scale": 0.2,
                "acc_scale": 0.2,
                "approach_dz": 0.10,
                "use_orientation_constraint": True,
                "execute": execute_moves,
            },
        ],
        # arguments=["--ros-args", "--log-level", "arm_controller:=debug"],
    )

    # Delay avoids racing move_group param publication
    delayed_arm_controller = TimerAction(period=7.0, actions=[arm_controller])

    return LaunchDescription([
        DeclareLaunchArgument("ur_type", default_value="ur5e"),
        DeclareLaunchArgument("robot_ip", default_value="192.168.0.100"),
        DeclareLaunchArgument("use_fake_hardware", default_value="true"),
        DeclareLaunchArgument("launch_rviz", default_value="true"),
        DeclareLaunchArgument("execute", default_value="false"),
        driver,
        moveit,
        delayed_arm_controller,
    ])
