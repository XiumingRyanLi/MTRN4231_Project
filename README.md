1. Table of Contents:

2. Project Overview:
   -video

3. System Architecture:
   - package level architecture diagram
   - behaviour tree showing closed loop
   - description of each node
   - custom message interface explainations

4. Technical Components:
   - Computer Vision:
   - Custom End-Effector:
   - System Visualisation:
   - Closed-Loop Operation:
  
---

# 5. Installation and Setup

This section explains how to install dependencies, build the workspace, configure the hardware, and prepare the system for running a full chess-playing session with the UR5e robot.

---

## 5.1 Software Prerequisites

The system has been tested on the following stack:

### **Operating System**
- Ubuntu 22.04 LTS  
- Real-time kernel NOT required

### **Robotics Framework**
- ROS 2 Humble Hawksbill  
- MoveIt 2 (installed through apt)

### **Development Tools**
```bash
sudo apt install python3-pip python3-colcon-common-extensions \
  build-essential cmake git python3-opencv
```

### **Python Dependencies**
```bash
pip install numpy opencv-python Pillow pyyaml scipy
```

### **Chess Engine**
- Stockfish (included in `stockfish/` folder)
- No external installation needed

### **Microcontroller**
- Arduino IDE OR arduino-cli for uploading the end-effector firmware

---

## 5.2 Cloning and Building the Workspace

```bash
# Create workspace
mkdir -p ~/mtrn4231_ws/src
cd ~/mtrn4231_ws/src

# Clone project
git clone <repo-url> chess_robot

# Build
cd ~/mtrn4231_ws
colcon build --symlink-install

# Source the environment
source install/setup.bash
```

Alternatively, the project includes a helper script:

```bash
cd chess_robot
./environment_setup.sh
```

This script:
- Installs required Python dependencies  
- Builds the ROS workspace  
- Sets up Stockfish paths  
- Automatically sources your ROS environment  

---

## 5.3 Hardware Setup

### **UR5e Robot**
- Connect the UR5e control box to the ROS PC via Ethernet.
- Assign static IPs in the same subnet (e.g., 192.168.0.x).
- Load the “External Control” URCap on the pendant.
- Set robot → ROS control target IP to the ROS machine.

### **Overhead Camera**
- Mount above board at a fixed perpendicular angle.
- Ensure entire 8×8 grid is visible with minimal distortion.
- Check camera enumeration:
```bash
ls /dev/video*
```

### **End-Effector / Gripper**
- Mount custom-designed gripper using UR5e flange adapter.
- Upload firmware:
```bash
arduino-cli upload -p /dev/ttyACM0 ArduinoCode.ino
```
- Test motion via serial:
  - `open` → fully open  
  - `close` → close enough to grip standard chess pieces  

### **Electrical**
- Ensure solid grounding between Arduino, UR5e controller, and sensing modules.
- USB isolation is recommended for noise immunity.

---

## 5.4 System Calibration

The following calibrations **must** be performed for accurate gameplay.

### **1. Hand–Eye Calibration (Camera → Robot Base TF)**
Defines transform:
```
camera_frame → chessboard_frame → robot_base_frame
```
Store final values in your TF broadcaster or YAML file.

### **2. Square Mapping**
`chess_square.py` defines coordinates of all 64 squares.

If board is moved or scaled, update values:
```python
square_coords["e4"] = [x, y, z]
```

### **3. Z-Height Calibration**
Use robot to probe:
- Top of board surface  
- Top of tallest piece  

These define approach heights and safe drop heights.

---

# 6. Running the System

This section describes how to launch, test, and interact with the full chess-robot pipeline.

---

## 6.1 Full-System Launch (Recommended)

From project root:

```bash
./launch.sh
```

This launches:
- UR5e driver  
- MoveIt planning pipeline  
- Perception stack  
- Chess logic + Stockfish  
- GUI  

To use a multi-window tmux interface:

```bash
./launch_tmux.sh
```

---

## 6.2 Component-Level Launch (For Debugging)

### **Terminal 1 — MoveIt + UR5e Control**
```bash
ros2 launch <moveit_package> moveit_rviz.launch.py
```

### **Terminal 2 — Vision**
```bash
ros2 run vision chess_detector
```

### **Terminal 3 — Game Coordinator**
```bash
ros2 run chess_controller master.py
```

### **Terminal 4 — GUI**
```bash
python3 gui_test.py
```

---

## 6.3 What Should Happen During Execution

- RViz displays live UR5e joint states.
- Vision node detects board grid and pieces.
- GUI shows:
  - Board state  
  - Current turn  
  - Legal moves  
  - Stockfish recommendations  

### **When a move is executed:**
1. The system verifies legality.
2. The planner generates collision-free pick trajectory.
3. The gripper picks piece from source square.
4. The robot moves to destination.
5. Vision system double-checks placement.
6. Game state updates.

---

## 6.4 Troubleshooting Guide

### **Robot not moving**
- check in Rviz that the robot is simulated 
- UR5e not in Remote Control mode.
- IP mismatch between URCap → ROS driver.
- MoveIt failing to find a collision-free path.

### **Camera not publishing**
```bash
ros2 topic list | grep image
```
If no result appears:
- Missing drivers  
- USB bandwidth exceeded  

### **Squares misaligned**
- Open Rviz and add a image topic
- Inside the image topic select image/cropped
- Adjust the board on the table such that it is inside the frame

### **Gripper fails to pick pieces**
- Recalibrate open/close PWM values in `ArduinoCode.ino`. The value are set in by the task coordinator, verfiy 
- Ensure robot approach height is not too low/too high.

---

# 7. Results and Demonstration:

# 8. Discussion and Future Improvements

Several engineering challenges emerged during development:

### **Perception**
- Lighting drastically affects board detection.
- Shadows cause false piece detections.
- Future versions:  
  - Use AprilTags or ArUco grids  
  - Integrate depth sensing (Realsense or ZED)  

### **Motion Planning**
- The UR5e must avoid collisions with tall pieces.  
- Some diagonal pieces require more complex approach trajectories.  
- Future upgrade:  
  - Use pilz industrial planner for deterministic paths  
  - Add dynamic obstacle detection  

### **End-Effector Performance**
- Suction or magnetic grippers could improve reliability.
- Current servo mechanism works but is sensitive to alignment.

### **System Integration**
- TF tree maintenance is critical.  
- Minor calibration drift significantly impacts accuracy.  
- Future upgrade: automated calibration routine.

---

# 9. Contributors

| Member | Contribution |
|--------|--------------|
| **Ryan Li** | MoveIt integration, URDF/xacro modeling, motion planning, system bring-up, TF integration, gripper implementation|
| **Johnnie Parris** | Vision pipeline, depth transforms, perception → TF integration |
| **Justin Kwok** | Game engine integration, Stockfish communication, task coordination, GUI, gripper implementation|

Additional support was received in lab sessions from course staff.

---

# 10. Repository Structure

```
.
├── src/                         # ROS 2 packages (moveit config, drivers, vision, chess controller)
├── stockfish/                   # Stockfish chess engine binary & weights
├── ArduinoCode.ino              # Gripper firmware (servo control + motion presets)
├── board.png                    # Calibration board image
├── chess_square.py              # Coordinates of 64 physical board squares
├── environment_setup.sh         # Setup script (deps + build + env)
├── gui_test.py                  # Standalone GUI for board visualisation
├── kill_all.sh                  # Terminates all ROS + python nodes
├── launch.sh                    # One-command full system launcher
├── launch_tmux.sh               # Multi-window launcher for debugging
├── master.py                    # High-level game logic + motion sequencing
└── robot arm movement steps.txt # Internal motion notes for trajectory design
```

---

# 11. References & Acknowledgements

### **Frameworks and Libraries**
- ROS 2 Humble  
- MoveIt 2 Planning Framework  
- UR5e ROS 2 Driver  
- OpenCV for vision  
- Stockfish chess engine  

### **Academic Resources**
- MTRN4231 Robotics Course Notes  
- UR5e technical documentation  
- ROS 2 TF2 tutorials on camera calibration  

### **Special Thanks**
- MTRN4231 teaching team for ongoing support  
- Lab demonstrators David Nie and Alex Cronin for guidance and assistance  
- Fellow student teams for collaboration and shared testing time Nail Bot and Jenga Bot

---

    

