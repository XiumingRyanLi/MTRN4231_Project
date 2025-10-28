from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
import os

def generate_launch_description():
    pkg = 'ur5e_robot_config'
    use_rviz = LaunchConfiguration('use_rviz', default='true')

    # Paths
    from ament_index_python.packages import get_package_share_directory
    share = get_package_share_directory(pkg)
    urdf = os.path.join(share, 'urdf', 'ur5e.urdf.xacro')
    srdf = os.path.join(share, 'srdf', 'ur5e.srdf')
    kinematics = os.path.join(share, 'config', 'kinematics.yaml')
    ompl = os.path.join(share, 'config', 'ompl_planning.yaml')
    mctrl = os.path.join(share, 'config', 'moveit_controllers.yaml')
    r2ctrl = os.path.join(share, 'config', 'ros2_controllers.yaml')
    rviz_cfg = os.path.join(share, 'rviz', 'ur5e_moveit.rviz')

    robot_description = Command(['xacro ', urdf])

    # Robot State Publisher
    rsp = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # Controllers (manager + broadcaster + trajectory ctrl)
    cm = Node(
        package='controller_manager', executable='ros2_control_node',
        parameters=[{'robot_description': robot_description}, r2ctrl],
        output='screen'
    )

    jsb = Node(
        package='controller_manager', executable='spawner',
        arguments=['joint_state_broadcaster'], output='screen'
    )

    traj = Node(
        package='controller_manager', executable='spawner',
        arguments=['scaled_joint_trajectory_controller'], output='screen'
    )

    # MoveIt move_group
    move_group = Node(
        package='moveit_ros_move_group', executable='move_group',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
            {'robot_description_semantic': open(srdf).read()},
            kinematics, ompl, mctrl
        ]
    )

    rviz = Node(
        package='rviz2', executable='rviz2',
        arguments=['-d', rviz_cfg],
        condition=IfCondition(use_rviz)
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_rviz', default_value='true'),
        rsp, cm, jsb, traj, move_group, rviz
    ])
