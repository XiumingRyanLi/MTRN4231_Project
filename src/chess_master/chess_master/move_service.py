from interfaces.srv import ChessMove
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int32
from array import array
import threading
import rclpy
from rclpy.node import Node
import chess
import chess.engine
import chess.svg
import cairosvg
from std_msgs.msg import String

ENGINE_PATH = "./stockfish/stockfish"


class ChessMaster(Node):

    def __init__(self):
        super().__init__('chess_master')

        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
        self.lock = threading.Lock()
        self.last_fen = None

        self.srv = self.create_service(
            ChessMove, 'chess_move', self.service_callback)

        self.status_pub = self.create_publisher(String, 'status', 10)
        self.pub = self.create_publisher(CompressedImage, 'board_state', 10)

        self.current_skill = 20
        self.engine.configure({"Skill Level": self.current_skill})
        self.skill_sub = self.create_subscription(Int32, 'skill_level', self.skill_callback, 10)

        self.timer = self.create_timer(0.1, self.pub_callback)

    def pub_callback(self):
        with self.lock:
            fen = self.board.fen()
            # Skip publish if nothing changed since last tick
            if fen == self.last_fen:
                return
            self.last_fen = fen

            # Export SVG and convert to PNG
            svg = chess.svg.board(board=self.board, size=480)
            # output_path = os.path.expanduser("~/MTRN4231_Project/board.png")
            png_bytes = cairosvg.svg2png(bytestring=svg.encode("utf-8"))

            # Publish PNG
            msg = CompressedImage()
            msg.format = "png"
            # msg.data = png_bytes
            msg.data = array('B', png_bytes)
            self.pub.publish(msg)
            

    def is_valid_fen(self, fen: str) -> bool:
        try:
            chess.Board(fen)
            return True
        except ValueError:
            return False

    def service_callback(self, request, response):
        text = request.user_move
        self.get_logger().info(f'Incoming request: {text}')

        with self.lock:
            # Set board with FEN
            if self.is_valid_fen(text):
                self.board = chess.Board(text)
                self.get_logger().info("Board updated to given FEN!")
                response.robot_move = "Board set"
                return response

            # Board reset check
            if text.lower() == "reset":
                self.board.reset()
                response.robot_move = "Board reset"
                self.get_logger().info("Board reset.")
                return response

            # Promotion check (for white only)
            if len(text) < 4:
                response.robot_move = "Error: Invalid move format (e.g. use 'e2e4' or 'e7e8q' for promotion)"
                msg = String()
                msg.data = "Invalid move format (e.g. use 'e2e4' or 'e7e8q' for promotion)"
                self.status_pub.publish(msg)
                return response

            if len(text) == 4:
                from_sq = chess.parse_square(text[:2])
                piece = self.board.piece_at(from_sq)
                if text[1] == '7' and text[3] == '8':
                    if piece and piece.piece_type == chess.PAWN:
                        text += "q"  # default to queen promotion

            # Move user piece
            try:
                move = chess.Move.from_uci(text)
            except ValueError:
                response.robot_move = "Error: Invalid move format (e.g. use 'e2e4' or 'e7e8q' for promotion)"
                msg = String()
                msg.data = "Invalid move format (e.g. use 'e2e4' or 'e7e8q' for promotion)"
                self.status_pub.publish(msg)
                return response

            if move not in self.board.legal_moves:
                response.robot_move = 'Error: Illegal move in current state'
                msg = String()
                msg.data = 'Error: Illegal move in current state'
                self.status_pub.publish(msg)
                return response

            self.board.push(move)

            # Check if game is over
            if self.board.is_game_over():
                outcome = self.board.outcome()
                if outcome:
                    response.robot_move = f"Game over: {outcome.result()} ({outcome.termination.name.lower()})"
                    msg = String()
                    msg.data = f"Game over: {outcome.result()} ({outcome.termination.name.lower()})"
                    self.status_pub.publish(msg)
                else:
                    response.robot_move = "Game over"
                    msg = String()
                    msg.data = "Game over"
                    self.status_pub.publish(msg)
                return response

            # Engine play next move
            result = self.engine.play(self.board, chess.engine.Limit(time=1))
            best_move = result.move

            response.robot_move = best_move.uci()
            self.get_logger().info(f"Next move: {best_move.uci()}")

            # Check for special move
            response.is_en_passant = False
            response.is_castling = False
            response.is_promotion = False
            response.is_capture = False
            if self.board.is_en_passant(best_move):
                response.is_en_passant = True
            if self.board.is_capture(best_move):
                response.is_capture = True
            if self.board.is_castling(best_move):
                response.is_castling = True
            if best_move.promotion:
                response.is_promotion = True

            self.board.push(best_move)

        return response

    def skill_callback(self, msg):
        lvl = max(0, min(20, int(msg.data)))  # clamp to [0, 20]
        if lvl != self.current_skill:
            self.current_skill = lvl
            self.engine.configure({"Skill Level": lvl})
            self.get_logger().info(f"Updated Stockfish Skill Level → {lvl}")
            msg = String()
            msg.data = f"Updated Stockfish Skill Level → {lvl}"
            self.status_pub.publish(msg)

    def destroy_node(self):
        try:
            if self.engine is not None:
                self.engine.quit()
        except Exception:
            pass
        super().destroy_node()


def main():
    rclpy.init()

    node = ChessMaster()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
