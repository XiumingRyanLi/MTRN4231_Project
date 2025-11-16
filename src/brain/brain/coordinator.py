import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from custom_interfaces.srv import ChessMove
from custom_interfaces.action import GripperCommand

# Define corner coordinates
A1 = (309, -818.0)
H1 = (309, -519.9)
A8 = (4.9, -818.0)
H8 = (4.9, -519.9)

# Define pieces height
KING_HEIGHT = 180
PAWN_HEIGHT = 153.6


class TaskCoordinator(Node):

    def __init__(self):
        super().__init__('task_coordinator')

        # listens to chess move from GUI
        self.move_sub_ = self.create_subscription(
            String, 'move_finish', self.listener_callback, 10)

        # subscribes to /player_move
        self.player_move_sub = self.create_subscription(
            String, 'player_move', self.move_callback, 10)

        # create chess master client
        self.client = self.create_client(ChessMove, 'chess_move')

        # gripper action client
        self.gripper_client = ActionClient(
            self, GripperCommand, 'gripper/command')

        # moveit action client
        # TODO

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

    def move_callback(self, msg):
        move = msg.data
        self.get_logger().info(f"Detected move: {move}")

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
        self.get_logger().info(
            f"is_tall_piece_from: {resp.is_tall_piece_from}")
        self.get_logger().info(f"is_tall_piece_to: {resp.is_tall_piece_to}")

        # Figure robot arm movement steps
        self.get_logger().info("== Robot Arm Movement Steps ==")
        robot_move = resp.robot_move
        if len(robot_move) < 4 or len(robot_move) > 5:
            return

        sq1 = robot_move[0:2]
        sq2 = robot_move[2:4]
        x1, y1 = self.get_real_world_coords(sq1)
        x2, y2 = self.get_real_world_coords(sq2)
        from_piece_is_tall = resp.is_tall_piece_from
        to_piece_is_tall = resp.is_tall_piece_to

        # case en passant
        if resp.is_en_passant:
            self.normal_move(x1, y1, x2, y2, sq1, sq2, PAWN_HEIGHT)
            # sq2 same file + 1 rank
            pawn_sq = sq2[0] + '4'
            pawnx, pawny = self.get_real_world_coords(pawn_sq)
            self.discard_piece(pawnx, pawny, pawn_sq, PAWN_HEIGHT)
            return
        # case capture
        if resp.is_capture:
            if to_piece_is_tall:
                self.discard_piece(x2, y2, sq2, KING_HEIGHT)
            else:
                self.discard_piece(x2, y2, sq2, PAWN_HEIGHT)
            if resp.is_promotion:
                self.discard_piece(x1, y1, sq1, PAWN_HEIGHT)
                self.promote_piece(x2, y2, sq2, KING_HEIGHT)
            else:
                if from_piece_is_tall:
                    self.normal_move(x1, y1, x2, y2, sq1, sq2, KING_HEIGHT)
                else:
                    self.normal_move(x1, y1, x2, y2, sq1, sq2, PAWN_HEIGHT)
            return
        # case castling
        if resp.is_castling:
            self.normal_move(x1, y1, x2, y2, sq1, sq2, KING_HEIGHT)
            # check which rook to move (works for white only for now)
            if sq2 == 'g8':
                rookx1, rooky1 = self.get_real_world_coords('h8')
                rookx2, rooky2 = self.get_real_world_coords('f8')
                self.normal_move(rookx1, rooky1, rookx2,
                                 rooky2, 'h8', 'f8', PAWN_HEIGHT)
            if sq2 == 'c8':
                rookx1, rooky1 = self.get_real_world_coords('a8')
                rookx2, rooky2 = self.get_real_world_coords('d8')
                self.normal_move(rookx1, rooky1, rookx2,
                                 rooky2, 'a8', 'd8', PAWN_HEIGHT)
            return
        # case promotion
        if resp.is_promotion:
            self.discard_piece(x1, y1, sq1, PAWN_HEIGHT)
            self.promote_piece(x2, y2, sq2, KING_HEIGHT)
            return

        if from_piece_is_tall:
            self.normal_move(x1, y1, x2, y2, sq1, sq2, KING_HEIGHT)
        else:
            self.normal_move(x1, y1, x2, y2, sq1, sq2, PAWN_HEIGHT)

    def get_real_world_coords(self, square: str):

        # Extract file (A-H) and rank (1-8)
        file = square[0].upper()
        rank = int(square[1])

        if file not in "ABCDEFGH" or rank not in range(1, 9):
            raise ValueError("Invalid square. Use like 'e4' or 'A1'.")

        # Calculate step size
        dx_per_file = (H1[0] - A1[0]) / 7
        dy_per_file = (H1[1] - A1[1]) / 7
        dx_per_rank = (A8[0] - A1[0]) / 7
        dy_per_rank = (A8[1] - A1[1]) / 7

        # Compute offsets
        file_index = ord(file) - ord('A')
        rank_index = rank - 1

        x = A1[0] + file_index * dx_per_file + rank_index * dx_per_rank
        y = A1[1] + file_index * dy_per_file + rank_index * dy_per_rank

        return x, y

    def normal_move(self, x1, y1, x2, y2, sq1, sq2, h):
        self.get_logger().info(f"Move to {x1}, {y1}, {h} ({sq1})")
        # TODO: call arm controller
        self.send_gripper_goal(close=True, effort=8.0)
        self.get_logger().info(f"Move to {x2}, {y2}, {h} ({sq2})")
        # TODO: call arm controller
        # artificially add 3 seconds
        self.send_gripper_goal(close=False, effort=8.0)

    def discard_piece(self, x, y, sq, h):
        self.get_logger().info(f"Move to {x}, {y}, {h} ({sq})")
        # TODO: call arm controller
        self.send_gripper_goal(close=True, effort=8.0)
        self.get_logger().info("Move to discard pile")
        # TODO: call arm controller
        self.send_gripper_goal(close=False, effort=8.0)

    def promote_piece(self, x, y, sq, h):
        self.get_logger().info("Move to extra queen")
        # TODO: call arm controller
        self.send_gripper_goal(close=True, effort=8.0)
        self.get_logger().info(f"Move to {x}, {y}, {h} ({sq})")
        # TODO: call arm controller
        self.send_gripper_goal(close=False, effort=8.0)

    def send_gripper_goal(self, close: bool, effort: float = 0.0):
        if not self.gripper_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("Gripper action server not available")
            return

        goal_msg = GripperCommand.Goal()
        goal_msg.close = close          # True = close, False = open
        goal_msg.effort = effort        # 0.0 means "ignore effort" in your bridge

        self.get_logger().info(
            f"Sending gripper goal: close={close}, effort={effort:.3f}"
        )

        # Send goal asynchronously; we get a Future for the goal handle
        send_future = self.gripper_client.send_goal_async(
            goal_msg,
            feedback_callback=self._gripper_feedback_cb
        )
        send_future.add_done_callback(self._gripper_goal_response_cb)

    def _gripper_goal_response_cb(self, future):
        try:
            goal_handle = future.result()
        except Exception as e:
            self.get_logger().error(f"Gripper goal send failed: {e}")
            return

        if not goal_handle.accepted:
            self.get_logger().warn("Gripper goal was rejected by server")
            return

        self.get_logger().info("Gripper goal accepted")

        # Ask for the result asynchronously
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._gripper_result_cb)

    def _gripper_feedback_cb(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f"Gripper feedback: {fb.progress_percent:.1f}% — {fb.stage}"
        )

    def _gripper_result_cb(self, future):
        """Called once the gripper action is finished (success, abort, or cancel)."""
        try:
            result = future.result().result
        except Exception as e:
            self.get_logger().error(f"Gripper result retrieval failed: {e}")
            return

        self.get_logger().info(
            f"Gripper finished: success={result.success}, message='{result.message}'"
        )


def main(args=None):
    rclpy.init(args=args)
    node = TaskCoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
