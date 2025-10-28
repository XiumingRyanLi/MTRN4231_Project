from interfaces.srv import ChessMove

import threading
import rclpy
from rclpy.node import Node
import chess
import chess.engine
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

        self.pub = self.create_publisher(String, 'board_state', 10)

        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        with self.lock:
            fen = self.board.fen()
            # Skip publish if nothing changed since last tick
            if fen == self.last_fen:
                return
            self.last_fen = fen

            msg = String()
            msg.data = str(self.board)
            self.pub.publish(msg)

    def is_valid_fen(self, fen: str) -> bool:
        try:
            chess.Board(fen)
            return True
        except ValueError:
            return False

    def service_callback(self, request, response):
        text = request.confirm
        print(text)
        self.get_logger().info(f'Incoming request: {text}')

        with self.lock:
            # Set board with FEN
            if self.is_valid_fen(text):
                self.board = chess.Board(text)
                self.get_logger().info("Board updated to given FEN!")
                response.chess_move = "Board set"
                return response

            # Board reset check
            if text.lower() == "reset":
                self.board.reset()
                response.chess_move = "Board reset"
                self.get_logger().info("Board reset.")
                return response

            # Promotion check (for white only)
            if len(text) < 4:
                response.chess_move = "Error: Invalid move format (e.g. use 'e2e4' or 'e7e8q' for promotion)"
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
                response.chess_move = "Error: Invalid move format (e.g. use 'e2e4' or 'e7e8q' for promotion)"
                return response

            if move not in self.board.legal_moves:
                response.chess_move = 'Error: Illegal move in current state'
                return response

            self.board.push(move)

            # Engine play next move
            result = self.engine.play(self.board, chess.engine.Limit(time=1))
            best_move = result.move

            response.chess_move = best_move.uci()
            self.get_logger().info(f"Next move: {best_move.uci()}")

            self.board.push(best_move)

        return response

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
