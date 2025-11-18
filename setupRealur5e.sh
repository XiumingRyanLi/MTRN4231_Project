gnome-terminal -t "DriverServer" -e 'ros2 launch ur_robot_driver ur_control.launch.py \
    ur_type:=ur5e \
    robot_ip:=192.168.0.100 \
    initial_joint_controller:=scaled_joint_trajectory_controller \
    use_fake_hardware:=false \
    launch_rviz:=false \
    description_package:=ur5e_custom_description \
    description_file:=ur5e_with_tool.urdf.xacro'

sleep 5

gnome-terminal --title="MoveitServer" -- bash -lc "
  set -e
  source /opt/ros/humble/setup.bash
  cd '$WS_ROOT'
  source install/setup.bash || true

  ros2 launch ${MOVEIT_PKG} ur_moveit.launch.py \
    ur_type:=${UR_TYPE} \
    description_package:=${DESC_PKG} \
    description_file:=${DESC_FILE} \
    moveit_config_package:=${MOVEIT_PKG} \
    moveit_config_file:=${MOVEIT_SRDF_FILE} \
    use_fake_hardware:=true \
    launch_rviz:=true

  status=\$?
  echo
  echo 'MoveitServer exited with code' \$status
  echo 'Press Enter to close...'
  read
"


# launch arm controller 
ros2 launch arm_controller arm_controller.launch.py execute:=true
