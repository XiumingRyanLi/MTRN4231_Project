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
        self.get_logger().info("== Robot Arm Movement Steps ==")
        robot_move = resp.robot_move
        if len(robot_move) < 4 or len(robot_move) > 5:
            return
        
        sq1 = robot_move[0:2]
        sq2 = robot_move[2:4]
        x1, y1 = self.get_real_world_coords(sq1)
        x2, y2 = self.get_real_world_coords(sq2)
        
        # case en passant
        if resp.is_en_passant:
            self.normal_move(x1, y1, x2, y2, sq1, sq2)
            # sq2 same file + 1 rank
            pawn_sq = sq2[0] + '4'
            pawnx, pawny = self.get_real_world_coords(pawn_sq)
            self.discard_piece(pawnx, pawny, pawn_sq)
            return
        # case capture
        if resp.is_capture:
            self.discard_piece(x2, y2, sq2)
            if resp.is_promotion:
                self.discard_piece(x1, y1, sq1)
                self.promote_piece(x2, y2, sq2)
            else:
                self.normal_move(x1, y1, x2, y2, sq1, sq2)
            return
        # case castling
        if resp.is_castling:
            self.normal_move(x1, y1, x2, y2, sq1, sq2)
            # check which rook to move
            if sq2 == 'g8':
                rookx1, rooky1 = self.get_real_world_coords('h8')
                rookx2, rooky2 = self.get_real_world_coords('f8')
                self.normal_move(rookx1, rooky1, rookx2, rooky2, 'h8', 'f8')
            if sq2 == 'c8':
                rookx1, rooky1 = self.get_real_world_coords('a8')
                rookx2, rooky2 = self.get_real_world_coords('d8')
                self.normal_move(rookx1, rooky1, rookx2, rooky2, 'a8', 'd8')
            return
        # case promotion
        if resp.is_promotion:
            self.discard_piece(x1, y1, sq1)
            self.promote_piece(x2, y2, sq2)
            return

        self.normal_move(x1, y1, x2, y2, sq1, sq2)

    def get_real_world_coords(self, square: str):
        # Define corner coordinates
        A1 = (309, -818.0)
        H1 = (309, -519.9)
        A8 = (4.9, -818.0)
        H8 = (4.9, -519.9)

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

    def normal_move(self, x1, y1, x2, y2, sq1, sq2):
        self.get_logger().info(f"Move to {x1}, {y1} ({sq1})")
        self.get_logger().info(f"Grip")
        self.get_logger().info(f"Move to {x2}, {y2} ({sq2})")
        self.get_logger().info(f"Ungrip")
        
    def discard_piece(self, x, y, sq):
        self.get_logger().info(f"Move to {x}, {y} ({sq})")
        self.get_logger().info(f"Grip")
        self.get_logger().info(f"Move to discard pile")
        self.get_logger().info(f"Ungrip")
        
    def promote_piece(self, x, y, sq):
        self.get_logger().info(f"Move to extra queen")
        self.get_logger().info(f"Grip")
        self.get_logger().info(f"Move to {x}, {y} ({sq})")
        self.get_logger().info(f"Ungrip")


def main(args=None):
    rclpy.init(args=args)
    node = TaskCoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
