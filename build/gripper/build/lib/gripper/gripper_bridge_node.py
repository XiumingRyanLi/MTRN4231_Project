#!/usr/bin/env python3
import re
import time
import threading
from typing import Optional, Tuple

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.executors import MultiThreadedExecutor

from serial import Serial, SerialException
from serial.tools import list_ports

# Import your action
from custom_interfaces.action import GripperCommand  # <-- change to your package

STATE_RE = re.compile(r"STATE\s+open=(?P<open>[01]),\s*force=(?P<force>-?\d+(?:\.\d+)?)")

def now_ms() -> int:
    return int(time.time() * 1000)

class SerialGripperBridge(Node):
    """
    ActionServer: your_interfaces_pkg/GripperCommand
    Goal:   close(bool), effort(float64)
    Result: success(bool), message(string)
    Feedback: progress_percent(float64), stage(string)
    """

    def __init__(self):
        super().__init__('gripper_bridge')

        # -------- Parameters --------
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baud', 115200)
        self.declare_parameter('open_is', 1)      # Arduino 'open' state numeric (0/1)
        self.declare_parameter('read_timeout_s', 0.1)
        self.declare_parameter('write_retries', 3)
        self.declare_parameter('command_timeout_s', 8.0)   # time allowed to reach target state
        self.declare_parameter('verify_period_s', 0.2)
        self.declare_parameter('auto_find_usb', True)      # if port missing, try to auto-find

        self._port = self.get_parameter('port').get_parameter_value().string_value
        self._baud = self.get_parameter('baud').get_parameter_value().integer_value
        self._open_is = self.get_parameter('open_is').get_parameter_value().integer_value
        self._read_timeout = float(self.get_parameter('read_timeout_s').value)
        self._write_retries = int(self.get_parameter('write_retries').value)
        self._command_timeout = float(self.get_parameter('command_timeout_s').value)
        self._verify_period = float(self.get_parameter('verify_period_s').value)
        self._auto_find_usb = bool(self.get_parameter('auto_find_usb').value)

        # -------- Serial --------
        self._ser_lock = threading.Lock()
        self._ser: Optional[Serial] = None
        self._reader_thread = threading.Thread(target=self._serial_reader_loop, daemon=True)
        self._stop_event = threading.Event()

        # Most-recent parsed state (updated by reader thread)
        self._last_open: Optional[int] = None
        self._last_force: Optional[float] = None
        self._last_line_ts_ms: int = 0

        self._connect_serial()
        self._reader_thread.start()

        # -------- Action Server --------
        self._action_server = ActionServer(
            self,
            GripperCommand,
            'gripper/command',
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
        )

        self.get_logger().info("gripper_bridge ready (Action: gripper/command).")

    # ---------- Action Server Callbacks ----------
    def goal_cb(self, goal_request: GripperCommand.Goal) -> GoalResponse:
        # Always accept; you can add concurrency checks if needed.
        self.get_logger().info(f"Goal received: close={goal_request.close}, effort={goal_request.effort:.3f}")
        return GoalResponse.ACCEPT

    def cancel_cb(self, _goal_handle) -> CancelResponse:
        # Try to stop any ongoing motion gracefully if your firmware supports it.
        self._send_line("CMD STOP\n")
        self.get_logger().warn("Cancel requested → sent CMD STOP")
        return CancelResponse.ACCEPT

    async def execute_cb(self, goal_handle):
        goal: GripperCommand.Goal = goal_handle.request
        target_open = 0 if goal.close else 1  # desired 'open' bit on Arduino
        stage = "initializing"

        # Optional effort (send before the command if given)
        if goal.effort and goal.effort > 0.0:
            self._send_with_retries(f"EFFORT {goal.effort:.3f}\n")

        cmd = "CMD CLOSE\n" if goal.close else "CMD OPEN\n"
        if not self._send_with_retries(cmd):
            result = GripperCommand.Result(success=False, message="Failed to write command to serial")
            goal_handle.abort()
            return result

        start_ms = now_ms()
        last_feedback_ms = 0
        stage = "executing"

        # Poll/stream state until we reach the target, or timeout/cancel
        while rclpy.ok():
            if goal_handle.is_cancel_requested:
                self._send_line("CMD STOP\n")
                goal_handle.canceled()
                return GripperCommand.Result(success=False, message="Canceled")

            # Ask for state explicitly to keep fresh updates flowing
            self._send_line("QRY STATE\n")

            # Read the most recent parsed state snapshot
            open_bit, force_val, age_ms = self._snapshot_state()

            # Determine progress heuristic:
            #   - if we haven't seen any state yet, progress ~5%
            #   - when in-motion but not arrived, progress ramps up to 90%
            #   - when arrived, set to 100%
            arrived = (open_bit is not None and open_bit == target_open)
            elapsed = (now_ms() - start_ms) / max(self._command_timeout, 0.001)
            ramp = max(0.05, min(0.90, elapsed))  # 5%..90%

            progress = 1.0 if arrived else ramp
            progress_percent = float(int(progress * 100.0))

            # Publish feedback at ~5 Hz
            if now_ms() - last_feedback_ms > 200:
                fb = GripperCommand.Feedback()
                fb.progress_percent = progress_percent
                fb.stage = "verifying" if arrived else stage
                goal_handle.publish_feedback(fb)
                last_feedback_ms = now_ms()

            if arrived:
                msg = f"{'Closed' if goal.close else 'Opened'} OK (force={force_val:.3f})" if force_val is not None else \
                      f"{'Closed' if goal.close else 'Opened'} OK"
                result = GripperCommand.Result(success=True, message=msg)
                goal_handle.succeed()
                return result

            # Timeout?
            if (now_ms() - start_ms) / 1000.0 > self._command_timeout:
                result = GripperCommand.Result(success=False, message="Timeout waiting for target state")
                goal_handle.abort()
                return result

            # Wait a bit before next verify
            await self._async_sleep(self._verify_period)

    async def _async_sleep(self, seconds: float):
        # rclpy doesn't provide an awaitable sleep, so just spin time slices
        end_t = time.time() + seconds
        while time.time() < end_t:
            await rclpy.task.Future()  # yield to executor

    # ---------- Serial helpers ----------
    def _connect_serial(self):
        port = self._port
        if self._auto_find_usb and (not port or port == '/dev/ttyUSB0'):
            # Try to pick the first ttyUSB/ttyACM if default is missing
            candidates = [p.device for p in list_ports.comports() if ('ttyUSB' in p.device or 'ttyACM' in p.device)]
            if candidates:
                port = candidates[0]
                self.get_logger().warn(f"Auto-selected serial port: {port}")
        try:
            self._ser = Serial(port, self._baud, timeout=self._read_timeout)
            self.get_logger().info(f"Opened serial: {port} @ {self._baud}")
        except SerialException as e:
            self._ser = None
            self.get_logger().error(f"Serial open failed on {port}: {e}")

    def _serial_reader_loop(self):
        buf = bytearray()
        while not self._stop_event.is_set():
            try:
                if self._ser is None:
                    time.sleep(0.5)
                    self._connect_serial()
                    continue

                chunk = self._ser.read(64)  # small non-blocking read
                if not chunk:
                    continue
                buf.extend(chunk)
                # Split by newlines
                while b'\n' in buf:
                    line, _, rest = buf.partition(b'\n')
                    buf = bytearray(rest)
                    self._handle_serial_line(line.decode(errors='ignore').strip())

            except SerialException as e:
                self.get_logger().error(f"Serial read error: {e}; reconnecting…")
                with self._ser_lock:
                    try:
                        if self._ser:
                            self._ser.close()
                    except Exception:
                        pass
                    self._ser = None
                time.sleep(0.5)
            except Exception as e:
                self.get_logger().error(f"Reader loop error: {e}")
                time.sleep(0.1)

    def _handle_serial_line(self, line: str):
        # Expected forms: "ACK <something>", "STATE open=1,force=7.2"
        if not line:
            return

        m = STATE_RE.match(line)
        if m:
            self._last_open = int(m.group('open'))
            self._last_force = float(m.group('force'))
            self._last_line_ts_ms = now_ms()
            return

        # You can parse other lines if your firmware emits them:
        # if line.startswith("ACK"):
        #     self.get_logger().debug(f"Arduino: {line}")

    def _snapshot_state(self) -> Tuple[Optional[int], Optional[float], int]:
        # Returns (open_bit, force, age_ms)
        age = now_ms() - self._last_line_ts_ms if self._last_line_ts_ms else 1_000_000
        return self._last_open, self._last_force, age

    def _send_line(self, s: str) -> bool:
        with self._ser_lock:
            if not self._ser:
                return False
            try:
                self._ser.write(s.encode('utf-8'))
                return True
            except SerialException as e:
                self.get_logger().error(f"Serial write error: {e}")
                try:
                    self._ser.close()
                except Exception:
                    pass
                self._ser = None
                return False

    def _send_with_retries(self, s: str) -> bool:
        for i in range(self._write_retries):
            if self._send_line(s):
                return True
            self.get_logger().warn(f"Write retry {i+1}/{self._write_retries} for: {s.strip()}")
            time.sleep(0.1)
        return False

    # ---------- Shutdown ----------
    def destroy_node(self):
        self._stop_event.set()
        try:
            if self._ser:
                self._ser.close()
        except Exception:
            pass
        super().destroy_node()


def main():
    rclpy.init()
    node = SerialGripperBridge()
    try:
        executor = MultiThreadedExecutor()
        rclpy.spin(node, executor=executor)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
