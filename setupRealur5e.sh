gnome-terminal -t "DriverServer" -e 'ros2 launch ur_robot_driver ur_control.launch.py \
    ur_type:=ur5e \
    robot_ip:=192.168.0.100 \
    initial_joint_controller:=joint_trajectory_controller \
    use_fake_hardware:=false \
    launch_rviz:=false \
    description_package:=ur5e_custom_description \
    description_file:=ur5e_with_tool.urdf.xacro'

sleep 10

gnome-terminal -t "MoveitServer" -e 'ros2 launch ur_moveit_config_custom ur_moveit.launch.py \
    robot_ip:=192.168.0.100 \
    ur_type:=ur5e \
    launch_rviz:=true \
    use_fake_hardware:=false \
    description_package:=ur5e_custom_description \
    description_file:=ur5e_with_tool.urdf.xacro'

sleep 10


# launch arm controller 
ros2 launch arm_controller arm_controller.launch.py execute:=true
