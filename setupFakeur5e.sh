gnome-terminal -t "DriverServer" -e 'ros2 launch ur_robot_driver ur_control.launch.py \
    ur_type:=ur5e \
    robot_ip:=yyy.yyy.yyy.yyy \
    initial_joint_controller:=joint_trajectory_controller \
    use_fake_hardware:=true \
    launch_rviz:=false \
    description_package:=ur5e_custom_description \
    description_file:=ur5e_with_tool.urdf.xacro'
sleep 5

gnome-terminal -t "MoveitServer" -e 'ros2 launch ur_moveit_config_custom ur_moveit.launch.py \
    ur_type:=ur5e \
    launch_rviz:=true \
    use_fake_hardware:=true \
    description_package:=ur5e_custom_description \
    description_file:=ur5e_with_tool.urdf.xacro'
    
sleep 5

ros2 launch arm_controller arm_controller.launch.py