#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from control_msgs.action import GripperCommand

class MockGripperServer(Node):
    def __init__(self):
        super().__init__('mock_gripper_server')
        self._server = ActionServer(
            self, GripperCommand, '/gripper_controller/gripper_cmd',
            execute_callback=self.execute_cb)

    async def execute_cb(self, goal_handle):
        goal = goal_handle.request.command
        self.get_logger().info(f'[MOCK] Target width={goal.position:.3f} m, max_effort={goal.max_effort:.1f} N')
        await self._sleep(0.8)
        goal_handle.succeed()
        return GripperCommand.Result()

    async def _sleep(self, secs):
        # non-blocking sleep
        end = self.get_clock().now().nanoseconds + int(secs*1e9)
        while self.get_clock().now().nanoseconds < end:
            rclpy.spin_once(self, timeout_sec=0.05)

def main():
    rclpy.init()
    node = MockGripperServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
