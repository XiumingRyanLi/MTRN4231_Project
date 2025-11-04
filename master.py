"""Chess master program"""

import chess
import chess.engine

ENGINE_PATH = "./stockfish/stockfish"


def main():
    """main function"""
    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
    board = chess.Board()
    while True:
        user_input = input("What's your next move? (in UCI): ")
        if user_input == "quit":
            break

        try:
            move = chess.Move.from_uci(user_input)
            if move not in board.legal_moves:
                print("Illegal move")
                continue
            board.push(move)

        except ValueError:
            print("Invalid move format. Use UCI notation (e.g. e2e4).")
            continue

        result = engine.play(board, chess.engine.Limit(time=1))
        best_move = result.move
        print("Stockfish plays:", best_move)

        board.push(best_move)
        print(board)

    engine.quit()


if __name__ == "__main__":
    main()
