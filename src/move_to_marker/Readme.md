colcon build --packages-select move_to_marker
source install/setup.bash
ros2 launch move_to_marker bringup_moveit_ur5e.launch.py

eg command:
ros2 topic pub /target_pose geometry_msgs/msg/PoseStamped "{
  header: {frame_id: base_link},
  pose: { position: {x: 0.40, y: 0.20, z: 0.25},
          orientation: {x: 1.0, y: 0.0, z: 0.0, w: 0.0} }
}"
