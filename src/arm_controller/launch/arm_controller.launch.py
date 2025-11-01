# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument, TimerAction
# from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, FindExecutable
# from launch_ros.substitutions import FindPackageShare
# from launch_ros.actions import Node

# def generate_launch_description():
#     execute_moves = LaunchConfiguration("execute")   # true => execute through controller
#     ur_type       = LaunchConfiguration("ur_type")   # keep overridable

#     ur_description   = FindPackageShare("ur_description")
#     ur_moveit_config = FindPackageShare("ur_moveit_config")

#     urdf_xacro = PathJoinSubstitution([ur_description,   "urdf", "ur.urdf.xacro"])
#     srdf_xacro = PathJoinSubstitution([ur_moveit_config, "srdf", "ur.srdf.xacro"])

#     joint_limits_yaml = PathJoinSubstitution([ur_description, "config", "ur5e", "joint_limits.yaml"])
#     kin_params_yaml   = PathJoinSubstitution([ur_description, "config", "ur5e", "default_kinematics.yaml"])
#     phys_params_yaml  = PathJoinSubstitution([ur_description, "config", "ur5e", "physical_parameters.yaml"])
#     vis_params_yaml   = PathJoinSubstitution([ur_description, "config", "ur5e", "visual_parameters.yaml"])
#     kinematics_yaml   = PathJoinSubstitution([ur_moveit_config, "config", "kinematics.yaml"])

#     robot_description_cmd = Command([
#         PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
#         urdf_xacro, " ",
#         "ur_type:=", ur_type, " ",
#         "name:=", "ur", " ",              # -> groups are 'ur_manipulator', etc.
#         "prefix:=", '""', " ",
#         "safety_limits:=", "true", " ",
#         "safety_pos_margin:=", "0.15", " ",
#         "safety_k_position:=", "20", " ",
#         "joint_limit_params:=", joint_limits_yaml, " ",
#         "kinematics_params:=", kin_params_yaml, " ",
#         "physical_params:=",  phys_params_yaml, " ",
#         "visual_params:=",    vis_params_yaml,
#     ])

#     robot_semantic_cmd = Command([
#         PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
#         srdf_xacro, " ",
#         "name:=", "ur", " ",
#         "prefix:=", '""'
#     ])

#     arm_controller = Node(
#         package="arm_controller",
#         executable="arm_controller_node",
#         name="arm_controller",
#         output="screen",
#         parameters=[
#             {"robot_description": robot_description_cmd},
#             {"robot_description_semantic": robot_semantic_cmd},
#             kinematics_yaml,  # defines 'robot_description_kinematics'
#             {
#                 "planning_group": "ur_manipulator",  # <-- key fix
#                 "base_frame": "base_link",
#                 "tcp_link": "tool0",
#                 "vel_scale": 0.2,
#                 "acc_scale": 0.2,
#                 "approach_dz": 0.10,
#                 "use_orientation_constraint": True,
#                 "execute": execute_moves,
#             },
#         ],
#     )

#     # small delay so move_group & params are up
#     delayed = TimerAction(period=5.0, actions=[arm_controller])

#     return LaunchDescription([
#         DeclareLaunchArgument("ur_type", default_value="ur5e"),
#         DeclareLaunchArgument("execute", default_value="true"),
#         delayed,
#     ])

import launch
import os
import sys

from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
from launch_ros.substitutions import FindPackageShare

def get_robot_description():
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
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare("ur_description"), "urdf", "ur.urdf.xacro"]),
            " ",
            "robot_ip:=172.17.0.2",
            " ",
            "joint_limit_params:=",
            joint_limit_params,
            " ",
            "kinematics_params:=",
            kinematics_params,
            " ",
            "physical_params:=",
            physical_params,
            " ",
            "visual_params:=",
            visual_params,
            " ",
           "safety_limits:=",
            "true",
            " ",
            "safety_pos_margin:=",
            "0.15",
            " ",
            "safety_k_position:=",
            "20",
            " ",
            "name:=",
            "ur",
            " ",
            "ur_type:=",
            "ur5e",
            " ",
            "prefix:=",
            '""',
            " ",
        ]
    )


    robot_description = {"robot_description": robot_description_content}
    return robot_description

def get_robot_description_semantic():
    # MoveIt Configuration
    robot_description_semantic_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare("ur_moveit_config"), "srdf", "ur.srdf.xacro"]),
            " ",
            "name:=",
            # Also ur_type parameter could be used but then the planning group names in yaml
            # configs has to be updated!
            "ur",
            " ",
            "prefix:=",
            '""',
            " ",
        ]
    )
    robot_description_semantic = {
        "robot_description_semantic": robot_description_semantic_content
    }
    return robot_description_semantic
    
def generate_launch_description():
    # generate_common_hybrid_launch_description() returns a list of nodes to launch
    robot_description = get_robot_description()
    robot_description_semantic = get_robot_description_semantic()
    demo_node = Node(
        package="arm_controller",
        executable="arm_controller_node",
        name="arm_controller",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
        ],
    )

    return launch.LaunchDescription([demo_node])