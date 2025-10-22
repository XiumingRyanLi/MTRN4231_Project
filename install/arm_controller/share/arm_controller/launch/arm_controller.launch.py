from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="arm_controller",
            executable="arm_controller_node",
            name="arm_controller",
            parameters=["/workspace/ros2_ws/src/arm_controller/config/params.yaml"],  # edit path or install config
            output="screen",
        )
    ])
