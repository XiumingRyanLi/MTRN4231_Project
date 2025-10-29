from interfaces.srv import ChessMove
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from PIL import Image, ImageTk
import io
import rclpy
from rclpy.node import Node
import tkinter as tk
from rclpy.executors import SingleThreadedExecutor


class UserInterface(tk.Tk):

    def __init__(self):
        # initiate GUI window
        super().__init__()
        self.title("Chess Client")
        self.geometry("500x650")  # window size

        self.move_label = tk.Label(self, text="Enter UCI move (e.g., e2e4):")
        self.move_label.pack(pady=(12, 4))

        self.move_entry = tk.Entry(self, width=20)
        self.move_entry.pack()

        frame = tk.Frame(self)
        frame.pack(pady=8)
        self.send_btn = tk.Button(
            frame, text="Move!", command=self.on_send)
        self.send_btn.pack(side="left", padx=5)
        self.reset_btn = tk.Button(
            frame, text="Reset Board", command=self.reset_press)
        self.reset_btn.pack(side="left", padx=5)

        self.status = tk.Label(self, text="Ready.")
        self.status.pack(pady=(4, 8))

        self.board_label = tk.Label(self)
        self.board_label.pack(pady=(12, 8), fill="both", expand=True)

        # initialize ROS node
        rclpy.init()
        self.node = rclpy.create_node('user_interface_gui')
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.node)

        # create chess master client
        self.client = self.node.create_client(ChessMove, 'chess_move')
        self.future = None
        self.req = ChessMove.Request()

        # create board state subscriber
        # self.sub = self.node.create_subscription(
        #     String, 'board_state', self.listener_callback, 10)
        self.sub = self.node.create_subscription(
            CompressedImage, 'board_state', self.listener_callback, 10)

        # Poll ROS without blocking
        self.after(20, self._spin_once)

    def listener_callback(self, msg):
        image = Image.open(io.BytesIO(msg.data))
        tk_image = ImageTk.PhotoImage(image)
        self.board_label.config(image=tk_image)
        self.board_label.image = tk_image  # prevent garbage collection

    def on_send(self):
        # validate move input
        move = self.move_entry.get().strip()
        if not move:
            self.status.config(text="Please enter a move.")
            return

        self.send_btn.config(state="disabled")
        self.status.config(text="Thinking...")
        self.req.user_move = move
        self.future = self.client.call_async(self.req)

        self.move_entry.delete(0, tk.END)

    def reset_press(self):
        # reset board
        self.req.user_move = "reset"
        self.future = self.client.call_async(self.req)

        self.move_entry.delete(0, tk.END)

    def _spin_once(self):
        # let ROS process callbacks
        self.executor.spin_once(timeout_sec=0.0)
        # check if service completed
        if self.future and self.future.done():
            try:
                result = self.future.result()
                self.status.config(text=f"Output: {result.robot_move}")
            except Exception as e:
                self.status.config(text=f"Service error: {e}")
            finally:
                self.future = None
                self.send_btn.config(state="normal")
        # schedule next poll
        self.after(20, self._spin_once)

    def destroy(self):
        # clean shutdown
        try:
            self.node.destroy_node()
        finally:
            rclpy.shutdown()
        super().destroy()


def main():
    app = UserInterface()
    app.mainloop()


if __name__ == '__main__':
    main()
