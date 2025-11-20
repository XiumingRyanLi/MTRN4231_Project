#!/bin/bash

source /opt/ros/humble/setup.bash
source ~/MTRN4231_Project/install/setup.bash

gnome-terminal --title="Chess Detector"    -- bash -c "ros2 run perception chess_detector; exec bash" &
gnome-terminal --title="State Comparison"  -- bash -c "ros2 run perception state_comparison; exec bash" &
gnome-terminal --title="User Interface"    -- bash -c "ros2 run ui user_interface; exec bash" &
gnome-terminal --title="Task Coordinator"  -- bash -c "ros2 run brain task_coordinator; exec bash" &
gnome-terminal --title="Chess Master"      -- bash -c "ros2 run chess_master master; exec bash" &

gnome-terminal --title="DriverServer" -- bash -c "ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur5e robot_ip:=192.168.0.100 use_fake_hardware:=false launch_rviz:=false; exec bash" &

sleep 5

gnome-terminal --title="MoveitServer" -- bash -c "ros2 launch ur_moveit_config ur_moveit.launch.py robot_ip:=192.168.0.100 ur_type:=ur5e launch_rviz:=true; exec bash" &

gnome-terminal --title="Arm Controller" -- bash -c "ros2 launch arm_controller arm_controller.launch.py execute:=true; exec bash" &

gnome-terminal --title="Gripper" -- bash -c "ros2 run gripper gripper_bridge --ros-args -p port:=/dev/ttyUSB0; exec bash" &
