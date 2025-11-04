# import launch
# import os
# import sys

# from launch_ros.actions import Node
# from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
# from launch_ros.substitutions import FindPackageShare
# from launch_ros.parameter_descriptions import ParameterValue   # <<< NEW

# def get_robot_description():
#     joint_limit_params = PathJoinSubstitution(
#         [FindPackageShare("ur_description"), "config", "ur5e", "joint_limits.yaml"]
#     )
#     kinematics_params = PathJoinSubstitution(
#         [FindPackageShare("ur_description"), "config", "ur5e", "default_kinematics.yaml"]
#     )
#     physical_params = PathJoinSubstitution(
#         [FindPackageShare("ur_description"), "config", "ur5e", "physical_parameters.yaml"]
#     )
#     visual_params = PathJoinSubstitution(
#         [FindPackageShare("ur_description"), "config", "ur5e", "visual_parameters.yaml"]
#     )

#     # Use the wrapper that includes UR + your end effector
#     wrapper_xacro = PathJoinSubstitution(
#         [FindPackageShare("arm_controller"), "urdf", "ur5e_with_tool.urdf.xacro"]
#     )

#     robot_description_content = Command(
#         [
#             PathJoinSubstitution([FindExecutable(name="xacro")]),
#             " ",
#             wrapper_xacro,
#             " ",
#             "robot_ip:=172.17.0.2",        # keep if you had this before
#             " ",
#             "joint_limit_params:=", joint_limit_params, " ",
#             "kinematics_params:=",  kinematics_params,  " ",
#             "physical_params:=",    physical_params,    " ",
#             "visual_params:=",      visual_params,      " ",
#             "safety_limits:=",      "true",             " ",
#             "safety_pos_margin:=",  "0.15",             " ",
#             "safety_k_position:=",  "20",               " ",
#             "name:=",               "ur",               " ",
#             "ur_type:=",            "ur5e",             " ",
#             "prefix:=",             '""',               " ",
#         ]
#     )

#     # <<< wrap as string >>>
#     robot_description = {
#         "robot_description": ParameterValue(robot_description_content, value_type=str)
#     }
#     return robot_description

# def get_robot_description_semantic():
#     robot_description_semantic_content = Command(
#         [
#             PathJoinSubstitution([FindExecutable(name="xacro")]),
#             " ",
#             PathJoinSubstitution([FindPackageShare("ur_moveit_config"), "srdf", "ur.srdf.xacro"]),
#             " ",
#             "name:=", "ur", " ",
#             "prefix:=", '""', " ",
#         ]
#     )
#     # <<< wrap as string >>>
#     return {
#         "robot_description_semantic": ParameterValue(
#             robot_description_semantic_content, value_type=str
#         )
#     }

# def generate_launch_description():
#     robot_description = get_robot_description()
#     robot_description_semantic = get_robot_description_semantic()

#     demo_node = Node(
#         package="arm_controller",
#         executable="arm_controller_node",
#         name="arm_controller",
#         output="screen",
#         parameters=[robot_description, robot_description_semantic],
#     )

#     return launch.LaunchDescription([demo_node])



# # import launch
# # import os
# # import sys

# # from launch_ros.actions import Node
# # from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
# # from launch_ros.substitutions import FindPackageShare

# # def get_robot_description():
# #     joint_limit_params = PathJoinSubstitution(
# #         [FindPackageShare("ur_description"), "config", "ur5e", "joint_limits.yaml"]
# #     )
# #     kinematics_params = PathJoinSubstitution(
# #         [FindPackageShare("ur_description"), "config", "ur5e", "default_kinematics.yaml"]
# #     )
# #     physical_params = PathJoinSubstitution(
# #         [FindPackageShare("ur_description"), "config", "ur5e", "physical_parameters.yaml"]
# #     )
# #     visual_params = PathJoinSubstitution(
# #         [FindPackageShare("ur_description"), "config", "ur5e", "visual_parameters.yaml"]
# #     )

# #     # <<< the only path change: call the wrapper xacro in arm_controller >>>
# #     wrapper_xacro = PathJoinSubstitution(
# #         [FindPackageShare("arm_controller"), "urdf", "ur5e_with_tool.urdf.xacro"]
# #     )

# #     robot_description_content = Command(
# #         [
# #             PathJoinSubstitution([FindExecutable(name="xacro")]),
# #             " ",
# #             wrapper_xacro,
# #             " ",
# #             "robot_ip:=172.17.0.2",
# #             " ",
# #             "joint_limit_params:=", joint_limit_params, " ",
# #             "kinematics_params:=",  kinematics_params,  " ",
# #             "physical_params:=",    physical_params,    " ",
# #             "visual_params:=",      visual_params,      " ",
# #             "safety_limits:=",      "true",             " ",
# #             "safety_pos_margin:=",  "0.15",             " ",
# #             "safety_k_position:=",  "20",               " ",
# #             "name:=",               "ur",               " ",
# #             "ur_type:=",            "ur5e",             " ",
# #             "prefix:=",             '""',               " ",
# #         ]
# #     )

# #     robot_description = {"robot_description": robot_description_content}
# #     return robot_description

# # def get_robot_description_semantic():
# #     robot_description_semantic_content = Command(
# #         [
# #             PathJoinSubstitution([FindExecutable(name="xacro")]),
# #             " ",
# #             PathJoinSubstitution([FindPackageShare("ur_moveit_config"), "srdf", "ur.srdf.xacro"]),
# #             " ",
# #             "name:=", "ur", " ",
# #             "prefix:=", '""', " ",
# #         ]
# #     )
# #     robot_description_semantic = {
# #         "robot_description_semantic": robot_description_semantic_content
# #     }
# #     return robot_description_semantic

# # def generate_launch_description():
# #     robot_description = get_robot_description()
# #     robot_description_semantic = get_robot_description_semantic()
# #     demo_node = Node(
# #         package="arm_controller",
# #         executable="arm_controller_node",
# #         name="arm_controller",
# #         output="screen",
# #         parameters=[
# #             robot_description,
# #             robot_description_semantic,
# #         ],
# #     )

# #     return launch.LaunchDescription([demo_node])

import launch
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

ROBOT_NAME = "ur5e_with_tool"   # must match URDF & SRDF

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

    wrapper_xacro = PathJoinSubstitution(
        [FindPackageShare("arm_controller"), "urdf", "ur5e_with_tool.urdf.xacro"]
    )

    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        wrapper_xacro, " ",
        "ur_type:=", "ur5e", " ",
        "name:=", ROBOT_NAME, " ",
        "prefix:=", '""', " ",
        "robot_ip:=", "192.168.0.100", " ",
        "joint_limit_params:=", joint_limit_params, " ",
        "kinematics_params:=",  kinematics_params,  " ",
        "physical_params:=",    physical_params,    " ",
        "visual_params:=",      visual_params,      " ",
        "safety_limits:=",      "true", " ",
        "safety_pos_margin:=",  "0.15",  " ",
        "safety_k_position:=",  "20",    " ",
    ])

    return {"robot_description": ParameterValue(robot_description_content, value_type=str)}

def get_robot_description_semantic():
    srdf_xacro = PathJoinSubstitution(
        [FindPackageShare("ur_moveit_config"), "srdf", "ur.srdf.xacro"]
    )
    robot_description_semantic_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        srdf_xacro, " ",
        "name:=", ROBOT_NAME, " ",
        "prefix:=", '""', " ",
    ])
    return {"robot_description_semantic": ParameterValue(robot_description_semantic_content, value_type=str)}

def generate_launch_description():
    robot_description = get_robot_description()
    robot_description_semantic = get_robot_description_semantic()

    # This one IS a ROS params file (has ros__parameters root)
    kinematics_yaml = PathJoinSubstitution(
        [FindPackageShare("ur_moveit_config"), "config", "kinematics.yaml"]
    )

    demo_node = Node(
        package="arm_controller",
        executable="arm_controller_node",
        name="arm_controller",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            kinematics_yaml,
            {
                # Make sure OMPL is the default pipeline
                "planning_pipelines": ["ompl"],
                "default_planning_pipeline": "ompl",

                # Your node’s own params
                "planning_group": "ur_manipulator",
                "base_frame": "base_link",
                "tcp_link": "tool0",
                "planner_id": "RRTConnectkConfigDefault",
                "execute": True,
            },
        ],
    )

    return launch.LaunchDescription([demo_node])

