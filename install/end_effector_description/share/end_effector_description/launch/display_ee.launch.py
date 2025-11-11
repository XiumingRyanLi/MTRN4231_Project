# end_effector_description/launch/display_ee.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg = 'end_effector_description'
    urdf_path = os.path.join(get_package_share_directory(pkg), 'urdf', 'end_effector.urdf.xacro')
    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    rviz_path = os.path.join(get_package_share_directory(pkg), 'rviz', 'ee.rviz')

    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             name='ee_robot_state_publisher',
             parameters=[{'robot_description': robot_description}], output='screen'),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             name='ee_joint_state_publisher_gui', output='screen'),
        Node(package='rviz2', executable='rviz2', name='ee_rviz2',
             arguments=['-d', rviz_path], output='screen'),
    ])

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='ee_robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='ee_joint_state_publisher_gui',
            output='screen',
        ),
        # NEW: publish world -> ee_mount (identity)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='ee_world_tf',
            arguments=['0', '0', '0', '0', '0', '0', 'world', 'ee_mount'],
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='ee_rviz2',
            arguments=['-d', rviz_path],   # your ee.rviz
            output='screen',
        ),
    ])
