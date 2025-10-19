# launch/chess_arm_executor.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg = get_package_share_directory('chess_arm_executor')
    default_params = os.path.join(pkg, 'config', 'chess_arm_executor.yaml')

    params_file = LaunchConfiguration('params_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'params_file',
            default_value=default_params,
            description='Path to YAML with node parameters.'
        ),
        Node(
            package='chess_arm_executor',
            executable='arm_controller_node',
            name='chess_arm_executor',
            output='screen',
            parameters=[params_file]
        )
    ])
