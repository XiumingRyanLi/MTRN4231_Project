#!/usr/bin/env python3
# gripper_bridge_node.py

import re
import time
import asyncio
import threading
from typing import Optional, Tuple

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.executors import MultiThreadedExecutor

from serial import Serial, SerialException
from serial.tools import list_ports

# ACTION TYPE: change if your interfaces pkg is different
from custom_interfaces.action import GripperCommand


def now_ms() -> int:
    return int(time.time() * 1000)


# Accept flexible Arduino outputs, e.g.:
#   STATE open=1,force=7.2
#   STATE OPEN=true FORCE=3.1
#   STATE open=0 force=7.2 progress=83
STATE_RE = re.compile(
    r"""(?ix)
    ^\s*STATE[:\s]*
    (?:
        (?=.*?\bopen\s*=\s*(?P<open>(?:0|1|true|false|open|closed)))
    )?
    (?:
        (?=.*?\bforce\s*=\s*(?P<force>-?\d+(?:\.\d+)?))
    )?
    (?:
        (?=.*?\bprogress\s*=\s*(?P<progress>\d{1,3}))
    )?
    .*$
    """
)


def parse_open_token(tok: str) -> int:
    v = (tok or "").strip().lower()
    if v in ("1", "true", "open", "opened"):
        return 1
    return 0


class SerialGripperBridge(Node):
    """
    ActionServer: custom_interfaces/GripperCommand
    Goal:   close(bool), effort(float64)
    Result: success(bool), message(string)
    Feedback: progress_percent(float64), stage(string)
    """

    def __init__(self):
        super().__init__("gripper_bridge")

        # ---------- Parameters ----------
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baud", 115200)
        self.declare_parameter("read_timeout_s", 0.1)
        self.declare_parameter("write_retries", 3)
        self.declare_parameter("command_timeout_s", 8.0)
        self.declare_parameter("verify_period_s", 0.2)
        self.declare_parameter("auto_find_usb", True)
        self.declare_parameter("invert_open_bit", False)  # flip meaning of 'open' if needed

        self._port = self.get_parameter("port").get_parameter_value().string_value
        self._baud = int(self.get_parameter("baud").value)
        self._read_timeout = float(self.get_parameter("read_timeout_s").value)
        self._write_retries = int(self.get_parameter("write_retries").value)
        self._command_timeout = float(self.get_parameter("command_timeout_s").value)
        self._verify_period = float(self.get_parameter("verify_period_s").value)
        self._auto_find_usb = bool(self.get_parameter("auto_find_usb").value)
        self._invert_open_bit = bool(self.get_parameter("invert_open_bit").value)

        # ---------- Serial state ----------
        self._ser_lock = threading.Lock()
        self._ser: Optional[Serial] = None
        self._stop_event = threading.Event()
        self._reader_thread = threading.Thread(target=self._serial_reader_loop, daemon=True)

        # Last parsed state (updated by reader thread)
        self._last_open: Optional[int] = None
        self._last_force: Optional[float] = None
        self._last_progress: Optional[float] = None
        self._last_line_ts_ms: int = 0
        self._last_unmatched_log: int = 0

        # Remember commanded target to improve DONE handling (optional)
        self._pending_target_open: Optional[int] = None

        # ---------- Connect & start reader ----------
        self._connect_serial()
        self._reader_thread.start()

        # ---------- Action Server ----------
        self._as = ActionServer(
            self,
            GripperCommand,
            "gripper/command",
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
        )

        self.get_logger().info("gripper_bridge is up (Action: /gripper/command)")

    # ===== Action callbacks =====
    def goal_cb(self, goal_request: GripperCommand.Goal) -> GoalResponse:
        self.get_logger().info(f"Goal received: close={goal_request.close}, effort={goal_request.effort:.3f}")
        return GoalResponse.ACCEPT

    def cancel_cb(self, _goal_handle) -> CancelResponse:
        self._send_line("CMD STOP\n")
        self.get_logger().warn("Cancel requested → sent CMD STOP")
        return CancelResponse.ACCEPT

    async def execute_cb(self, goal_handle):
        goal: GripperCommand.Goal = goal_handle.request
        target_open = 0 if goal.close else 1
        if self._invert_open_bit:
            target_open = 1 - target_open
        self._pending_target_open = target_open

        # Optional effort
        if goal.effort and goal.effort > 0.0:
            if not self._send_with_retries(f"EFFORT {goal.effort:.3f}\n"):
                res = GripperCommand.Result(success=False, message="Failed to send effort to serial")
                goal_handle.abort()
                return res

        # Send command
        cmd = "CMD CLOSE\n" if goal.close else "CMD OPEN\n"
        if not self._send_with_retries(cmd):
            res = GripperCommand.Result(success=False, message="Failed to write command to serial")
            goal_handle.abort()
            return res

        start_ms = now_ms()
        last_fb_ms = 0

        # Main wait/verify loop
        while rclpy.ok():
            if goal_handle.is_cancel_requested:
                self._send_line("CMD STOP\n")
                goal_handle.canceled()
                self._pending_target_open = None
                return GripperCommand.Result(success=False, message="Canceled")

            # Ask for fresh state (harmless if firmware streams anyway)
            self._send_line("QRY STATE\n")

            open_bit, force_val, age_ms = self._snapshot_state()
            bit = open_bit
            if bit is not None and self._invert_open_bit:
                bit = 1 - bit

            fresh = age_ms < 1000
            arrived = bool(fresh and bit is not None and bit == target_open)

            # Prefer firmware progress if provided & fresh
            if fresh and self._last_progress is not None:
                progress_percent = float(int(max(0.0, min(100.0, self._last_progress))))
            else:
                # fallback ramp 5%..90% based on elapsed time
                elapsed_s = (now_ms() - start_ms) / 1000.0
                ramp = max(0.05, min(0.90, elapsed_s / max(self._command_timeout, 0.001)))
                progress_percent = float(int(ramp * 100.0))

            stage = "verifying" if arrived else "executing"

            if now_ms() - last_fb_ms > 200:
                fb = GripperCommand.Feedback()
                fb.progress_percent = 100.0 if arrived else progress_percent
                fb.stage = stage
                goal_handle.publish_feedback(fb)
                last_fb_ms = now_ms()

            if arrived:
                msg = f"{'Closed' if goal.close else 'Opened'} OK"
                if force_val is not None:
                    msg += f" (force={force_val:.3f})"
                res = GripperCommand.Result(success=True, message=msg)
                goal_handle.succeed()
                self._pending_target_open = None
                return res

            if (now_ms() - start_ms) / 1000.0 > self._command_timeout:
                res = GripperCommand.Result(success=False, message="Timeout waiting for target state")
                goal_handle.abort()
                self._pending_target_open = None
                return res

            await asyncio.sleep(self._verify_period)

    # ===== Serial helpers =====
    def _connect_serial(self):
        port = self._port
        if self._auto_find_usb and (not port or port == "/dev/ttyUSB0"):
            cands = [p.device for p in list_ports.comports() if ("ttyUSB" in p.device or "ttyACM" in p.device)]
            if cands:
                port = cands[0]
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

                chunk = self._ser.read(128)
                if not chunk:
                    continue
                buf.extend(chunk)

                while b"\n" in buf:
                    line, _, rest = buf.partition(b"\n")
                    buf = bytearray(rest)
                    self._handle_serial_line(line.decode(errors="ignore").strip())

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
        if not line:
            return

        m = STATE_RE.match(line)
        if m:
            open_tok = m.group("open")
            force_tok = m.group("force")
            progress_tok = m.group("progress")

            if open_tok is not None:
                self._last_open = parse_open_token(open_tok)
            if force_tok is not None:
                try:
                    self._last_force = float(force_tok)
                except Exception:
                    pass
            if progress_tok is not None:
                try:
                    self._last_progress = max(0.0, min(100.0, float(progress_tok)))
                except Exception:
                    self._last_progress = None

            self._last_line_ts_ms = now_ms()
            return

        up = line.strip().upper()
        if up.startswith("DONE"):
            # If firmware emits DONE, assume we reached the pending target;
            # we don't flip bits here, we just refresh timestamp to make state "fresh".
            self._last_line_ts_ms = now_ms()
            return

        # Log unmatched lines occasionally to help adjust regex
        n = now_ms()
        if self._last_unmatched_log + 2000 < n:
            self.get_logger().warn(f"Unparsed serial line: '{line}'")
            self._last_unmatched_log = n

    def _snapshot_state(self) -> Tuple[Optional[int], Optional[float], int]:
        age = now_ms() - self._last_line_ts_ms if self._last_line_ts_ms else 1_000_000
        return self._last_open, self._last_force, age

    def _send_line(self, s: str) -> bool:
        with self._ser_lock:
            if not self._ser:
                return False
            try:
                self._ser.write(s.encode("utf-8"))
                return True
            except SerialException as e:
                self.get_logger().error(f"Serial write error: {e}")
                try:
                    if self._ser:
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

    # ===== Shutdown =====
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
        # MultiThreaded so the reader thread + executor cooperate nicely
        executor = MultiThreadedExecutor()
        rclpy.spin(node, executor=executor)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
