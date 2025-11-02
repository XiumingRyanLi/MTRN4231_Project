import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # same xacro you use in arm_controller.launch.py
    wrapper_xacro = PathJoinSubstitution(
        [FindPackageShare("arm_controller"), "urdf", "ur5e_with_tool.urdf.xacro"]
    )
    joint_limit_params = PathJoinSubstitution(
        [FindPackageShare("ur_description"), "config", "ur5e", "joint_limits.yaml"]
    )
    kinematics_params = PathJoinSubstitution(
        [FindPackageShare("ur_description"), "config", "ur5e", "default_kinematics.yaml"]
    )
    physical_params = PathJoinSubstitution(
        [FindPackageShare("ur_description"), "config", "ur5e", "physical_parameters.yaml"]
    )
    visual_params = PathJoinSubstitution(
        [FindPackageShare("ur_description"), "config", "ur5e", "visual_parameters.yaml"]
    )

    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        wrapper_xacro, " ",
        "joint_limit_params:=", joint_limit_params, " ",
        "kinematics_params:=",  kinematics_params,  " ",
        "physical_params:=",    physical_params,    " ",
        "visual_params:=",      visual_params,      " ",
        "safety_limits:=",      "true",             " ",
        "safety_pos_margin:=",  "0.15",             " ",
        "safety_k_position:=",  "20",               " ",
        "name:=",               "ur",               " ",
        "ur_type:=",            "ur5e",             " ",
        "prefix:=",             '""',               " ",
    ])
    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    rviz_config = PathJoinSubstitution(
        [FindPackageShare("arm_controller"), "rviz", "display.rviz"]
    )

    return LaunchDescription([
        # publish TF for the combined model
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="combined_robot_state_publisher",
            parameters=[robot_description],
            output="screen",
        ),
        # RViz
        Node(
            package="rviz2",
            executable="rviz2",
            name="combined_rviz",
            arguments=["-d", rviz_config],
            output="screen",
        ),
    ])
