import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from interfaces.srv import ChessMove


class TaskCoordinator(Node):

    def __init__(self):
        super().__init__('task_coordinator')

        # listens to chess move from GUI
        self.move_sub_ = self.create_subscription(
            String, 'move_finish', self.listener_callback, 10)

        # create chess master client
        self.client = self.create_client(ChessMove, 'chess_move')

    def listener_callback(self, msg):
        # validate move input
        move = (msg.data or '').strip()
        if not move:
            self.get_logger().info("Please enter a move.")
            return

        req = ChessMove.Request()
        req.user_move = move
        future = self.client.call_async(req)
        future.add_done_callback(self._on_response)

    def _on_response(self, future: rclpy.task.Future):
        try:
            resp: ChessMove.Response = future.result()
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
            return

        # Print response fields to terminal (ROS log)
        self.get_logger().info("")
        self.get_logger().info("== Chess Master Response ==")
        self.get_logger().info(f"Robot move: {resp.robot_move}")
        self.get_logger().info(f"is_en_passant: {resp.is_en_passant}")
        self.get_logger().info(f"is_capture: {resp.is_capture}")
        self.get_logger().info(f"is_castling: {resp.is_castling}")
        self.get_logger().info(f"is_promotion: {resp.is_promotion}")

        # Figure robot arm movement steps
        # case capture

        # case castling

        # case promotion

        # case en passant

        self.get_logger().info("== Robot Arm Movement Steps ==")


def main(args=None):
    rclpy.init(args=args)
    node = TaskCoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
