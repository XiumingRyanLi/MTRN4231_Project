import tkinter as tk
import re

UCI_RE = re.compile(r"^[a-h][1-8][a-h][1-8]([qrbn])?$")


class ChessClientGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Client")
        self.geometry("360x160")  # window size

        self.move_label = tk.Label(self, text="Enter UCI move (e.g., e2e4):")
        self.move_label.pack(pady=(12, 4))

        self.move_entry = tk.Entry(self, width=20)
        self.move_entry.pack()

        self.send_btn = tk.Button(self, text="Send", command=self.on_send)
        self.send_btn.pack(pady=8)

        self.status = tk.Label(self, text="Ready.")
        self.status.pack(pady=(4, 8))

    def fake_engine_reply(self, user_move: str) -> str:
        # Replace with actual ROS result later
        return "e7e5"

    def finish_reply(self, robot_move: str):
        self.status.config(text=f"Engine move: {robot_move}")
        self.send_btn.config(state="normal")

    def on_send(self):
        # validate move input
        move = self.move_entry.get().strip()
        if not move:
            self.status.config(text="Please enter a move.")
            return
        if not UCI_RE.match(move.lower()):
            self.status.config(text="Invalid UCI. Try e2e4 or a7a8q.")
            return
        self.status.config(text=f"Sent: {move} (pretend)")

        self.send_btn.config(state="disabled")
        self.status.config(text="Thinking...")
        # simulate latency
        self.after(1000, self.finish_reply, self.fake_engine_reply(move))


def main():
    app = ChessClientGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
