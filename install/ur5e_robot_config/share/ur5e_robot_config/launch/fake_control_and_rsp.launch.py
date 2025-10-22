from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_calib = DeclareLaunchArgument('kinematics_parameters_file', default_value='')
    calib = LaunchConfiguration('kinematics_parameters_file')

    pkg = get_package_share_directory('ur5e_robot_moveit')
    urdf = os.path.join(pkg, 'urdf', 'ur5e_with_tool.urdf.xacro')
    controllers = os.path.join(pkg, 'config', 'controllers.yaml')

    robot_description = {
        'robot_description': Command(['xacro ', urdf, ' kinematics_parameters_file:=', calib])
    }

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description],
        output='screen'
    )

    cm = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, controllers],
        output='screen'
    )

    jsb = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen'
    )

    jtc = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['scaled_joint_trajectory_controller', '--controller-manager', '/controller_manager'],
        output='screen'
    )

    return LaunchDescription([use_calib, rsp, cm, jsb, jtc])
