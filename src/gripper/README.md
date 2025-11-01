Gripper Node

# 1) Confirm the action type name
ros2 interface list | grep -i gripper
ros2 interface show custom_interfaces/action/GripperCommand

# 2) Send a goal (note the /action/ in the type)
ros2 action send_goal --feedback \
/gripper/command custom_interfaces/action/GripperCommand \
"{close: true, effort: 8.0}"

# Open:
ros2 action send_goal --feedback \
/gripper/command custom_interfaces/action/GripperCommand \
"{close: false, effort: 0.0}"