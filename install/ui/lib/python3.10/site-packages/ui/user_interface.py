from interfaces.srv import ChessMove
from std_msgs.msg import String
from std_msgs.msg import Int32
from sensor_msgs.msg import CompressedImage
from PIL import Image, ImageTk
import io
import rclpy
from rclpy.node import Node
import tkinter as tk
from tkinter import ttk
from rclpy.executors import SingleThreadedExecutor


class UserInterface(tk.Tk):

    def __init__(self):
        # initiate GUI window
        super().__init__()
        self.title("Chess Client")
        self.geometry("500x750")  # window size

        self.move_label = tk.Label(self, text="Enter UCI move (e.g., e2e4):")
        self.move_label.pack(pady=(12, 4))

        self.move_entry = tk.Entry(self, width=20)
        self.move_entry.pack()

        self.move_entry.bind("<Return>", lambda event: self.on_send())

        frame = tk.Frame(self)
        frame.pack(pady=8)
        self.send_btn = tk.Button(
            frame, text="Move!", command=self.on_send)
        self.send_btn.pack(side="left", padx=5)
        self.reset_btn = tk.Button(
            frame, text="Reset Board", command=self.reset_press)
        self.reset_btn.pack(side="left", padx=5)

        self.status_label = tk.Label(self)
        self.status_label.pack(pady=4)

        sep = ttk.Separator(self, orient='horizontal')
        sep.pack(fill="x", pady=10)

        lvl_frame = tk.Frame(self)
        lvl_frame.pack(pady=(4, 10))

        tk.Label(lvl_frame, text="Engine Skill Level (0–20):").pack(side="left", padx=(0, 8))

        # Create a variable to store the selected value
        self.skill_var = tk.StringVar(value="20")  # default value

        # Create dropdown list (Combobox)
        self.skill_combo = ttk.Combobox(
            lvl_frame,
            textvariable=self.skill_var,
            values=[str(i) for i in range(21)],
            state="readonly",
            width=4
        )
        self.skill_combo.pack(side="left")

        # When user selects a value, call this function
        self.skill_combo.bind("<<ComboboxSelected>>", self.on_skill_changed)

        self.board_label = tk.Label(self)
        self.board_label.pack(pady=(12, 8), fill="both", expand=True)

        # initialize ROS node
        rclpy.init()
        self.node = rclpy.create_node('user_interface_gui')
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.node)

        # create move publisher to task coordinator
        self.move_pub = self.node.create_publisher(String, 'move_finish', 10)

        # create skill level publisher
        self.skill_pub = self.node.create_publisher(Int32, 'skill_level', 10)

        # create status subscriber
        self.status_sub = self.node.create_subscription(String, 'status', self.status_callback, 10)

        # create board state subscriber
        self.sub = self.node.create_subscription(
            CompressedImage, 'board_state', self.listener_callback, 10)

        # Poll ROS without blocking
        self._spin_ros()
        # self.after(20, self._spin_once)

    def _spin_ros(self):
        # Run one non-blocking iteration of the executor, then schedule again
        try:
            self.executor.spin_once(timeout_sec=0.0)
        except Exception as e:
            print("Executor error:", e)
        self.after(10, self._spin_ros)  # every 10 ms (~100 Hz pump)

    def listener_callback(self, msg):
        image = Image.open(io.BytesIO(msg.data))
        tk_image = ImageTk.PhotoImage(image)
        self.board_label.config(image=tk_image)
        self.board_label.image = tk_image  # prevent garbage collection
        self.send_btn.config(state="normal")

    def status_callback(self, msg):
        self.status_label.config(text=msg.data)
        self.send_btn.config(state="normal")

    def on_send(self):
        # validate move input
        move = self.move_entry.get().strip()
        if not move:
            self.status.config(text="Please enter a move.")
            return

        self.send_btn.config(state="disabled")
        msg = String()
        msg.data = move
        self.move_pub.publish(msg)
        self.move_entry.delete(0, tk.END)

    def reset_press(self):
        # reset board
        msg = String()
        msg.data = "reset"
        self.move_pub.publish(msg)
        self.move_entry.delete(0, tk.END)

    def on_skill_changed(self, _event=None):
        self.publish_skill_level()

    def publish_skill_level(self):
        try:
            lvl = int(self.skill_var.get())
        except ValueError:
            lvl = 10
            self.skill_var.set("10")

        msg = Int32()
        msg.data = lvl
        self.skill_pub.publish(msg)

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
