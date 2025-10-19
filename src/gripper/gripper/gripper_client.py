#!/usr/bin/env python3
import json
import time
import serial
import threading

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from control_msgs.action import GripperCommand

class ArduinoGripperClient(Node):
    """
    - Subscribes:
        * gripper/grip_piece_type (std_msgs/String): e.g., "pawn", "rook", "queen"
        * gripper/release (std_msgs/String): any message triggers a release/open
    - Action Client:
        * /gripper_controller/gripper_cmd (control_msgs/action/GripperCommand)
    - Serial:
        * Sends ASCII lines to Arduino, e.g.:
            GRIP {"type":"pawn","width":0.028,"effort":25.0}
            RELEASE {}
    """

    def __init__(self):
        super().__init__('arduino_gripper_client')

        # ---- Parameters ----
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('gripper_action_name', '/gripper_controller/gripper_cmd')

        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value
        action_name = self.get_parameter('gripper_action_name').get_parameter_value().string_value

        # ---- Piece database (tune to your gripper & pieces) ----
        # width (m): target opening between fingertips to apply
        # effort (N): max effort for GripperCommand (interpreted by your controller)
        self.piece_db = {
            'pawn' :  {'diameter_mm': 22, 'height_mm': 35, 'width': 0.026, 'effort': 20.0},
            'knight': {'diameter_mm': 29, 'height_mm': 45, 'width': 0.030, 'effort': 25.0},
            'bishop': {'diameter_mm': 29, 'height_mm': 50, 'width': 0.030, 'effort': 25.0},
            'rook'  : {'diameter_mm': 31, 'height_mm': 45, 'width': 0.032, 'effort': 27.5},
            'queen' : {'diameter_mm': 33, 'height_mm': 55, 'width': 0.034, 'effort': 30.0},
            'king'  : {'diameter_mm': 35, 'height_mm': 60, 'width': 0.036, 'effort': 32.5},
        }

        self.current_piece = None  # stores the last piece command dict

        # ---- Serial (with a background reconnect loop) ----
        self._serial_lock = threading.Lock()
        self._ser = None
        self._serial_thread = threading.Thread(target=self._serial_connect_loop, args=(serial_port, baudrate), daemon=True)
        self._serial_thread.start()

        # ---- ROS I/O ----
        self.sub_piece = self.create_subscription(String, 'gripper/grip_piece_type',
                                                  self._piece_cmd_cb, 10)
        self.sub_release = self.create_subscription(String, 'gripper/release',
                                                    self._release_cb, 10)

        # Action client to the gripper
        self.gripper_ac = ActionClient(self, GripperCommand, action_name)

        self.get_logger().info(f'ArduinoGripperClient ready. Action: {action_name}, Serial: {serial_port}@{baudrate}')

    # ---------- Serial helpers ----------
    def _serial_connect_loop(self, port, baudrate):
        """Attempt to (re)connect to serial forever."""
        while rclpy.ok():
            if self._ser is None or not self._ser.is_open:
                try:
                    ser = serial.Serial(port, baudrate, timeout=0.5)
                    with self._serial_lock:
                        self._ser = ser
                    self.get_logger().info(f'Connected to Arduino on {port} at {baudrate} baud.')
                except Exception as e:
                    self.get_logger().warn(f'Failed to open serial {port}: {e}. Retrying in 2s...')
                    time.sleep(2.0)
                    continue
            time.sleep(1.0)

    def _serial_send_line(self, verb: str, payload: dict):
        """Send a single JSON line command to Arduino."""
        line = f'{verb} {json.dumps(payload)}\n'
        try:
            with self._serial_lock:
                if self._ser and self._ser.is_open:
                    self._ser.write(line.encode('utf-8'))
                else:
                    self.get_logger().warn('Serial not connected; skipping Arduino write.')
        except Exception as e:
            self.get_logger().warn(f'Error writing to serial: {e}')

    # ---------- Subscribers ----------
    def _piece_cmd_cb(self, msg: String):
        piece_type = msg.data.strip().lower()
        if piece_type not in self.piece_db:
            self.get_logger().error(f'Unknown piece type "{piece_type}". Known: {list(self.piece_db.keys())}')
            return

        piece = dict(self.piece_db[piece_type])  # copy
        piece['type'] = piece_type
        self.current_piece = piece  # store last command
        self.get_logger().info(f'Received grip request for piece: {piece_type} -> {piece}')

        # 1) Send action goal to the gripper controller
        self._send_gripper_goal(width=piece['width'], effort=piece['effort'])

        # 2) Send serial command to Arduino (so your micro can orchestrate sensors/closing profile/etc.)
        self._serial_send_line('GRIP', {"type": piece_type, "width": piece['width'], "effort": piece['effort']})

    def _release_cb(self, _msg: String):
        self.get_logger().info('Received RELEASE command.')
        # Open the gripper fully (pick a width larger than any piece)
        self._send_gripper_goal(width=0.050, effort=10.0)
        self._serial_send_line('RELEASE', {})

    # ---------- Action Client ----------
    def _send_gripper_goal(self, width: float, effort: float):
        """
        Sends a GripperCommand goal:
          - command.position = target gap (meters)
          - command.max_effort = limit (N)
        """
        if not self.gripper_ac.wait_for_server(timeout_sec=0.5):
            self.get_logger().warn('Gripper action server not available right now.')
            # Still send the serial command (already done in caller).
            return

        goal_msg = GripperCommand.Goal()
        goal_msg.command.position = float(width)
        goal_msg.command.max_effort = float(effort)

        self.get_logger().info(f'Sending gripper goal: width={width:.3f} m, effort={effort:.1f} N')

        send_future = self.gripper_ac.send_goal_async(
            goal_msg,
            feedback_callback=self._gripper_feedback_cb
        )
        send_future.add_done_callback(self._goal_response_cb)

    def _goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Gripper goal rejected.')
            return
        self.get_logger().info('Gripper goal accepted.')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._result_cb)

    def _gripper_feedback_cb(self, feedback_msg):
        # Feedback msg fields are implementation-specific for your controller; keep it generic
        # Some controllers mirror position/effort in feedback
        try:
            fb = feedback_msg.feedback
            # Not all servers populate these; guard with getattr
            pos = getattr(getattr(fb, 'position', fb), 'position', None)
            eff = getattr(getattr(fb, 'effort', fb), 'effort', None)
            if pos is not None or eff is not None:
                self.get_logger().debug(f'Gripper feedback: pos={pos} effort={eff}')
        except Exception:
            pass

    def _result_cb(self, future):
        result = future.result().result
        # Many implementations echo final position/effort; log generically
        self.get_logger().info('Gripper action finished.')

def main():
    rclpy.init()
    node = ArduinoGripperClient()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

# ros2 launch gripper gripper_bringup.launch.py serial_port:=/dev/ttyACM0 baudrate:=115200