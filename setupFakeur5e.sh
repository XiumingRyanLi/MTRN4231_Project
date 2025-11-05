cmd.exe /c start "UR Driver" wsl.exe -d "Ubuntu 22.04.5 LTS" ^


UR_TYPE=ur5e
DESC_PKG=ur5e_custom_description
DESC_FILE=ur5e_with_tool.urdf.xacro
# ROBOT_IP=127.0.0.1   # ignored in fake mode; harmless

# # 1) UR driver (fake hardware publishes /joint_states)
# gnome-terminal --title="UR Driver (fake)" -- bash -lc "
#   source /opt/ros/humble/setup.bash
#   source install/setup.bash
#   ros2 launch ur_robot_driver ur_control.launch.py \
#     ur_type:=${UR_TYPE} \
#     robot_ip:=${ROBOT_IP} \
#     initial_joint_controller:=joint_trajectory_controller \
#     use_fake_hardware:=true \
#     launch_rviz:=false \
#     description_package:=${DESC_PKG} \
#     description_file:=${DESC_FILE}
# "
# sleep 5

# # 2) MoveIt + RViz (interactive markers; same description)
# cmd.exe /c start "UR MoveIt" wsl.exe -d "Ubuntu 22.04.5 LTS" ^
# gnome-terminal --title="MoveIt + RViz" -- bash -lc "
#   source /opt/ros/humble/setup.bash
#   source install/setup.bash
#   ros2 launch ur_moveit_config ur_moveit.launch.py \
#     ur_type:=${UR_TYPE} \
#     use_fake_hardware:=true \
#     launch_rviz:=true \
#     description_package:=${DESC_PKG} \
#     description_file:=${DESC_FILE}
# "


# # 3) Your controller (rename if 'manipulation' is your package)



cmd.exe /c start "UR Driver" wsl.exe -d "Ubuntu 22.04.5 LTS" ^
bash -lc 'unset QT_SCALE_FACTOR; source /opt/ros/humble/setup.bash; 
ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur5e robot_ip:=yyy.yyy.yyy.yyy initial_joint_controller:=joint_trajectory_controller use_fake_hardware:=true launch_rviz:=false description_package:=ur5e_custom_description description_file:=ur5e_with_tool.urdf.xacro'

# wait a moment
sleep 5

# 2) MoveIt + RViz window
cmd.exe /c start "UR MoveIt" wsl.exe -d "Ubuntu 22.04.5 LTS" ^
bash -lc 'unset QT_SCALE_FACTOR; source /opt/ros/humble/setup.bash; 
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e use_fake_hardware:=true launch_rviz:=true description_package:=ur5e_custom_description description_file:=ur5e_with_tool.urdf.xacro'

sleep 5
ros2 launch arm_controller arm_controller.launch.py execute:=true