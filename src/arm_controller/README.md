The setup guide for MOVEIT packages


ping 192.168.0.100

./setupReal

 ros2 launch arm_controller moveit_rviz.launch.py ur_type:=ur5e use_fake_hardware:=true


# Terminal A: MoveIt + RViz (fake hardware)
ros2 launch arm_controller moveit_rviz.launch.py ur_type:=ur5e use_fake_hardware:=true

# Terminal B: your controller node (force Z-down, ignore yaw)
ros2 run arm_controller arm_controller_node --ros-args -p keep_yaw:=false

# Terminal C: send positions 
 # A: position only (orientation will be overwritten to "down")
ros2 action send_goal /arm/pick_place custom_interfaces/action/MoveTCP \
'{pick_pose:{header:{frame_id:base_link},pose:{position:{x:0.35,y:0.10,z:0.30}}}}'

# B: another position
ros2 action send_goal /arm/pick_place custom_interfaces/action/MoveTCP \
'{pick_pose:{header:{frame_id:base_link},pose:{position:{x:0.45,y:-0.15,z:0.30}}}}'

