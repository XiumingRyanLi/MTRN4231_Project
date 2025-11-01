# gripper — Serial Gripper Action Bridge (ROS 2 Humble)

Action server that talks to an Arduino over serial (`/dev/ttyUSB*`) and exposes:
## 1) WSL USB setup 

### In **PowerShell (Administrator)**
```powershell
usbipd list                           # find BUSID of your USB-Serial device (e.g., 2-2, VID:PID 0403:6001)
usbipd bind --busid 2-2               # first time or after reboot
usbipd attach --wsl --busid 2-2       # attach to your default WSL distro

In WSL (Ubuntu)
ls /dev/tty*
ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null

## 2) Build
colcon build --packages-select gripper --symlink-install
source install/setup.bash

ros2 pkg list | grep -i gripper
ros2 pkg prefix gripper
ros2 interface show custom_interfaces/action/GripperCommand   # adjust pkg name if different

## Launch or run
ros2 launch gripper gripper_bridge.launch.py

ros2 run gripper gripper_bridge_node --ros-args -p port:=/dev/ttyUSB0 -p baud:=115200 -p invert_open_bit:=false



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


## Arduino code test
CMD OPEN
CMD CLOSE
QRY STATE
CMD STOP

Control line is connected on D9