import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory

def _load_yaml(pkg: str, relpath: str):
    with open(os.path.join(get_package_share_directory(pkg), relpath), "r") as f:
        return yaml.safe_load(f)

def _load_text(pkg: str, relpath: str):
    with open(os.path.join(get_package_share_directory(pkg), relpath), "r") as f:
        return f.read()

def _build_nodes(context):
    # resolve args
    ur_type    = LaunchConfiguration('ur_type').perform(context)
    desc_pkg   = LaunchConfiguration('description_package').perform(context)
    desc_file  = LaunchConfiguration('description_file').perform(context)      # e.g. 'urdf/end_effector_withDriverSupport.xacro'
    cfg_pkg    = LaunchConfiguration('moveit_config_package').perform(context)
    srdf_file  = LaunchConfiguration('moveit_config_file').perform(context)    # e.g. 'config/end_effector_withDriverSupport.srdf'
    launch_rviz_subst = LaunchConfiguration('launch_rviz')
    use_fake_hw = LaunchConfiguration('use_fake_hardware').perform(context)

    # URDF via xacro → robot_description (force string)
    robot_description = {
        'robot_description': ParameterValue(
            Command([
                PathJoinSubstitution([FindExecutable(name='xacro')]),
                ' ',
                PathJoinSubstitution([FindPackageShare(desc_pkg), desc_file]),
                ' ',
                'ur_type:=', ur_type
            ]),
            value_type=str
        )
    }

    # SRDF is a plain file → read to string (NO xacro here)
    robot_description_semantic = {
        'robot_description_semantic': _load_text(cfg_pkg, srdf_file)
    }

    # Load YAML configs
    kinematics_yaml  = _load_yaml(cfg_pkg, 'config/kinematics.yaml')
    ompl_yaml        = _load_yaml(cfg_pkg, 'config/ompl_planning.yaml')
    controllers_yaml = _load_yaml(cfg_pkg, 'config/controllers.yaml')

    # Typical tweak: fake HW uses joint_trajectory_controller by default
    if use_fake_hw == 'true':
        if 'scaled_joint_trajectory_controller' in controllers_yaml:
            controllers_yaml['scaled_joint_trajectory_controller']['default'] = False
        if 'joint_trajectory_controller' in controllers_yaml:
            controllers_yaml['joint_trajectory_controller']['default'] = True

    ompl_pipeline = {
        'move_group': {
            'planning_plugin': 'ompl_interface/OMPLPlanner',
            'request_adapters': (
                'default_planner_request_adapters/AddTimeOptimalParameterization '
                'default_planner_request_adapters/FixWorkspaceBounds '
                'default_planner_request_adapters/FixStartStateBounds '
                'default_planner_request_adapters/FixStartStateCollision '
                'default_planner_request_adapters/FixStartStatePathConstraints'
            ),
            'start_state_max_bounds_error': 0.1,
        }
    }
    ompl_pipeline['move_group'].update(ompl_yaml)

    planning_scene_monitor = {
        'publish_planning_scene': True,
        'publish_geometry_updates': True,
        'publish_state_updates': True,
        'publish_transforms_updates': True,
    }

    rviz_cfg = PathJoinSubstitution([FindPackageShare(cfg_pkg), 'config', 'moveit.rviz'])

    rsp = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        name='robot_state_publisher', output='screen',
        parameters=[robot_description]
    )

    move_group = Node(
        package='moveit_ros_move_group', executable='move_group', output='screen',
        parameters=[
            robot_description,
            robot_description_semantic,
            kinematics_yaml,
            ompl_pipeline,
            {'moveit_simple_controller_manager': controllers_yaml,
             'moveit_controller_manager': 'moveit_simple_controller_manager/MoveItSimpleControllerManager'},
            planning_scene_monitor
        ]
    )

    rviz = Node(
        package='rviz2', executable='rviz2', name='rviz2', output='screen',
        arguments=['-d', rviz_cfg],
        parameters=[robot_description, robot_description_semantic, kinematics_yaml, ompl_pipeline],
        condition=IfCondition(launch_rviz_subst)
    )

    return [rsp, move_group, rviz]

def generate_launch_description():
    return LaunchDescription([

        DeclareLaunchArgument('ur_type', default_value='ur5e'),
        DeclareLaunchArgument('description_package', default_value='ur5e_moveit_config_custom'),
        DeclareLaunchArgument('description_file', default_value='urdf/end_effector_withDriverSupport.xacro'),
        DeclareLaunchArgument('moveit_config_package', default_value='ur5e_moveit_config_custom'),
        DeclareLaunchArgument('moveit_config_file', default_value='config/end_effector_withDriverSupport.srdf'),
        DeclareLaunchArgument('use_fake_hardware', default_value='true'),
        DeclareLaunchArgument('launch_rviz', default_value='true'),

        OpaqueFunction(function=_build_nodes),
    ])