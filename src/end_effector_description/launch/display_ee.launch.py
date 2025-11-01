import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg = 'end_effector_description'
    xacro_file = os.path.join(get_package_share_directory(pkg), 'urdf', 'end_effector.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    rviz_file = os.path.join(get_package_share_directory(pkg), 'rviz', 'ee.rviz')
    rviz_args = ['-d', rviz_file] if os.path.exists(rviz_file) else []

    return LaunchDescription([
        Node(
            name='ee_robot_state_publisher',                                # ← unique
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
        Node(
            name='ee_joint_state_publisher_gui',                            # ← unique
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=rviz_args,
            output='screen',
        ),
    ])
