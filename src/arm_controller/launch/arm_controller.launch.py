#!/usr/bin/env python3
import os
from pathlib import Path
import yaml

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, FindExecutable, Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def _yaml_or_empty(p):
    if not os.path.exists(p):
        return {}
    with open(p, "r") as f:
        return yaml.safe_load(f) or {}

def _with_spaces(base_list):
    """Ensure Command() tokens are separated by spaces."""
    out = []
    for i, t in enumerate(base_list):
        out.append(t)
        if i != len(base_list) - 1:
            out.append(" ")
    return out

def _setup(context, *args, **kwargs):
    arm_share   = FindPackageShare("arm_controller").perform(context)
    robot_pkg   = LaunchConfiguration("robot_pkg").perform(context)
    robot_share = FindPackageShare(robot_pkg).perform(context)

    urdf_xacro  = PathJoinSubstitution([robot_share, "urdf", LaunchConfiguration("urdf_xacro")]).perform(context)
    srdf_file   = PathJoinSubstitution([robot_share, "srdf", LaunchConfiguration("srdf")]).perform(context)

    ur_name          = LaunchConfiguration("ur_name").perform(context)              # e.g. "ur5e"
    use_fake_hw      = LaunchConfiguration("use_fake_hardware").perform(context)    # "true"/"false"
    xacro_extra      = LaunchConfiguration("xacro_extra").perform(context).strip()  # e.g. "prefix:=ur_ safety_limits:=true"

    # Build xacro args
    xacro_tokens = [
        FindExecutable(name="xacro"),
        urdf_xacro,
        f"name:={ur_name}",
        f"use_fake_hardware:={use_fake_hw}",
    ]
    if xacro_extra:
        xacro_tokens.extend(xacro_extra.split())

    robot_description = {
        "robot_description": ParameterValue(
            Command(_with_spaces(xacro_tokens)), value_type=str
        )
    }

    # SRDF (xacro or plain)
    if srdf_file.endswith(".xacro"):
        srdf_tokens = [
            FindExecutable(name="xacro"),
            srdf_file,
            f"name:={ur_name}",
        ]
        if xacro_extra:
            srdf_tokens.extend(xacro_extra.split())
        robot_semantic = {
            "robot_description_semantic": ParameterValue(
                Command(_with_spaces(srdf_tokens)), value_type=str
            )
        }
    else:
        with open(srdf_file, "r") as f:
            robot_semantic = {"robot_description_semantic": f.read()}

    # Config YAMLs
    cfg_dir     = Path(arm_share) / "config"
    kinematics  = _yaml_or_empty(str(cfg_dir / "kinematics.yaml"))
    controllers = _yaml_or_empty(str(cfg_dir / "moveit_controllers.yaml"))
    jointlims   = _yaml_or_empty(str(cfg_dir / "joint_limits.yaml"))
    pilzlims    = _yaml_or_empty(str(cfg_dir / "pilz_cartesian_limits.yaml"))

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[robot_description]
    )

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            robot_description,
            robot_semantic,
            {"robot_description_kinematics": kinematics},
            {"robot_description_planning": jointlims},
            {"pilz_cartesian_limits": pilzlims},
            {"moveit_controller_manager": "moveit_simple_controller_manager/MoveItSimpleControllerManager"},
            {"moveit_simple_controller_manager": controllers},
            {"planning_scene_monitor_options": {
                "name": "planning_scene_monitor",
                "publish_geometry_updates": True,
                "publish_state_updates": True,
                "publish_transforms_updates": True,
            }},
        ]
    )

    arm_node = Node(
        package="arm_controller",
        executable="arm_controller_node",
        name="arm_controller",
        output="screen",
        parameters=[
            robot_description,
            robot_semantic,
            {"planning_group": LaunchConfiguration("planning_group"),
             "base_frame": LaunchConfiguration("base_frame"),
             "tcp_link": LaunchConfiguration("tcp_link"),
             "vel_scale": LaunchConfiguration("vel_scale"),
             "acc_scale": LaunchConfiguration("acc_scale"),
             "approach_dz": LaunchConfiguration("approach_dz"),
             "planner_id": LaunchConfiguration("planner_id")}
        ]
    )

    return [rsp, move_group, arm_node]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("robot_pkg",   default_value="arm_controller",
                              description="Package that contains URDF/SRDF"),
        DeclareLaunchArgument("urdf_xacro",  default_value="ur5e_with_tool.urdf.xacro"),
        DeclareLaunchArgument("srdf",        default_value="ur5e_with_tool.srdf"),

        # xacro args
        DeclareLaunchArgument("ur_name",            default_value="ur5e"),
        DeclareLaunchArgument("use_fake_hardware",  default_value="true"),
        DeclareLaunchArgument("xacro_extra",        default_value=""),

        # controller/node params
        DeclareLaunchArgument("planning_group", default_value="manipulator"),
        DeclareLaunchArgument("base_frame",     default_value="base_link"),
        DeclareLaunchArgument("tcp_link",       default_value="tool0"),
        DeclareLaunchArgument("vel_scale",      default_value="0.2"),
        DeclareLaunchArgument("acc_scale",      default_value="0.2"),
        DeclareLaunchArgument("approach_dz",    default_value="0.10"),
        DeclareLaunchArgument("planner_id",     default_value=""),

        OpaqueFunction(function=_setup),
    ])
