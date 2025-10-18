from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Optional: place the 'board' frame; adjust to your setup
        Node(package='tf2_ros', executable='static_transform_publisher',
             arguments=['0.6','0.0','0.75','0','0','0','base_link','board']),

        Node(package='chess_arm_executor', executable='arm_controller_node', output='screen',
             parameters=['config/params.yaml'])
    ])
