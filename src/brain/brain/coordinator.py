import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String, Bool
from geometry_msgs.msg import PoseStamped
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import threading
import time
from custom_interfaces.srv import ChessMove
from custom_interfaces.action import GripperCommand, MoveTCP

# Define corner coordinates
A1 = (839.6, 302.1)
H1 = (538.0, 308.4)
A8 = (836.3, 0.3)
H8 = (534.8, 6.7)

# DISCARD/HOME coords
DISCARD_COORDS = (375.1, 149.8)
DISCARD_HEIGHT = 240.6

# Define pieces height
KING_HEIGHT = 178.0
PAWN_HEIGHT = 151.0
# KING_HEIGHT = 260.0 # (safe heights)
# PAWN_HEIGHT = 240.0 # (safe heights)


class TaskCoordinator(Node):

    def __init__(self):
        super().__init__('task_coordinator')

        # Allow callbacks to run concurrently
        self.cb_group = ReentrantCallbackGroup()

        # listens to chess move from GUI
        self.move_sub_ = self.create_subscription(
            String, 'move_finish', self.listener_callback, 10, callback_group=self.cb_group)

        # subscribes to /player_move
        self.player_move_sub = self.create_subscription(
            String, '/player_move', self.move_callback, 10, callback_group=self.cb_group)

        # take picture pub
        self.take_pic_pub = self.create_publisher(
            Bool, '/take_picture', 10)

        # create chess master client
        self.client = self.create_client(
            ChessMove, 'chess_move', callback_group=self.cb_group)

        # gripper action client
        self.gripper_client = ActionClient(
            self, GripperCommand, 'gripper/command', callback_group=self.cb_group)

        # moveit action client
        self.arm_client = ActionClient(
            self, MoveTCP, '/arm/pick_place', callback_group=self.cb_group)
        
        self.user_move = None
        self.is_user_piece_tall = None

    def listener_callback(self, msg):
        # validate move input
        move = (msg.data or '').strip()
        if not move:
            self.get_logger().info("Please enter a move.")
            return
        self.user_move = move
        self.get_logger().info(f"Detected move: {self.user_move}")
        req = ChessMove.Request()
        req.user_move = move
        future = self.client.call_async(req)
        future.add_done_callback(self._on_response)

    def move_callback(self, msg):
        self.user_move = msg.data
        self.get_logger().info(f"Detected move: {self.user_move}")

        req = ChessMove.Request()
        req.user_move = self.user_move
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
        self.get_logger().info(f"is_user_piece_tall: {resp.is_user_piece_tall}")
        self.get_logger().info(f"is_en_passant: {resp.is_en_passant}")
        self.get_logger().info(f"is_capture: {resp.is_capture}")
        self.get_logger().info(f"is_castling: {resp.is_castling}")
        self.get_logger().info(f"is_promotion: {resp.is_promotion}")
        self.get_logger().info(
            f"is_tall_piece_from: {resp.is_tall_piece_from}")
        self.get_logger().info(f"is_tall_piece_to: {resp.is_tall_piece_to}")
        self.get_logger().info(f"is_illegal: {resp.is_illegal}")


        # Figure robot arm movement steps
        self.get_logger().info("== Robot Arm Movement Steps ==")
        
        # User illegal moveback
        robot_move = resp.robot_move
        if resp.is_illegal:
            user_sq1 = self.user_move[0:2]
            user_sq2 = self.user_move[2:4]
            u_x1, u_y1 = self.get_real_world_coords(user_sq1)
            u_x2, u_y2 = self.get_real_world_coords(user_sq2)
            if resp.is_user_piece_tall:
                self.normal_move(u_x2, u_y2, u_x1, u_y1, user_sq2, user_sq1, KING_HEIGHT)
            else:
                self.normal_move(u_x2, u_y2, u_x1, u_y1, user_sq2, user_sq1, PAWN_HEIGHT)
            self.take_a_pic()
            return
        elif len(robot_move) < 4 or len(robot_move) > 5:
            return
        
        # Continue
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
            self.take_a_pic()
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
            self.take_a_pic()
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
            self.take_a_pic()
            return
        # case promotion
        if resp.is_promotion:
            self.discard_piece(x1, y1, sq1, PAWN_HEIGHT)
            self.promote_piece(x2, y2, sq2, KING_HEIGHT)
            self.take_a_pic()
            return

        if from_piece_is_tall:
            self.normal_move(x1, y1, x2, y2, sq1, sq2, KING_HEIGHT)
        else:
            self.normal_move(x1, y1, x2, y2, sq1, sq2, PAWN_HEIGHT)
        self.take_a_pic()

    def take_a_pic(self):
        # take picture
        msg = Bool()
        msg.data = False
        self.take_pic_pub.publish(msg)

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
        # Move to piece
        self.get_logger().info(f"Move to {x1}, {y1}, {h} ({sq1})")
        pick_pose = self.make_pose(x1, y1, h)
        ok = self.send_arm_goal(pick_pose, label=f"pick {sq1}")
        if not ok:
            self.get_logger().error(
                f"Arm failed to reach pick pose for {sq1}; aborting")
            return
        time.sleep(0.1)

        # Grip piece
        self.get_logger().info("Close gripper")
        ok = self.send_gripper_goal(close=True, effort=0.0)  # close gripper
        if not ok:
            self.get_logger().error("Gripper failed to close; aborting move")
            return
        time.sleep(0.1)

        # Move to new square
        self.get_logger().info(f"Move to {x2}, {y2}, {h} ({sq2})")
        pick_pose = self.make_pose(x2, y2, h)
        ok = self.send_arm_goal(pick_pose, label=f"place {sq2}")
        if not ok:
            self.get_logger().error(
                f"Arm failed to reach place pose for {sq2}; aborting")
            return
        time.sleep(0.1)

        # Ungrip piece
        self.get_logger().info("Open gripper")
        ok = self.send_gripper_goal(close=False, effort=0.0)  # open gripper
        if not ok:
            self.get_logger().error("Gripper failed to open")
        time.sleep(0.1)

        # move to home
        self.get_logger().info("Move to home")
        pick_pose = self.make_pose(
            DISCARD_COORDS[0], DISCARD_COORDS[1], DISCARD_HEIGHT)
        ok = self.send_arm_goal(pick_pose, label="go home")
        if not ok:
            self.get_logger().error("Arm failed to reach home; aborting")
            return
        time.sleep(0.1)

    def discard_piece(self, x, y, sq, h):
        # move to square 2
        self.get_logger().info(f"Move to {x}, {y}, {h} ({sq})")
        pick_pose = self.make_pose(x, y, h)
        ok = self.send_arm_goal(pick_pose, label=f"pick {sq}")
        if not ok:
            self.get_logger().error(
                f"Arm failed to reach pick pose for {sq}; aborting")
            return

        time.sleep(0.1)

        # close grip
        self.get_logger().info("Close gripper")
        ok = self.send_gripper_goal(close=True, effort=0.0)
        if not ok:
            self.get_logger().error("Failed to grip piece for discard")
            return
        time.sleep(0.1)

        # move to discard pile
        self.get_logger().info("Move to discard pile")
        pick_pose = self.make_pose(
            DISCARD_COORDS[0], DISCARD_COORDS[1], DISCARD_HEIGHT)
        ok = self.send_arm_goal(pick_pose, label="discard")
        if not ok:
            self.get_logger().error("Arm failed to discard; aborting")
            return
        time.sleep(0.1)

        # open grip
        self.get_logger().info("Open gripper")
        ok = self.send_gripper_goal(close=False, effort=0.0)
        if not ok:
            self.get_logger().error("Failed to grip piece for discard")
            return
        time.sleep(0.1)

    def promote_piece(self, x, y, sq, h):
        self.get_logger().info("Move to extra queen")
        # TODO: call arm controller

        # Close gripper
        self.get_logger().info("Close gripper")
        ok = self.send_gripper_goal(close=True, effort=0.0)
        if not ok:
            self.get_logger().error("Failed to grip queen")
            return
        time.sleep(0.1)

        # move to square
        self.get_logger().info(f"Move to {x}, {y}, {h} ({sq})")
        pick_pose = self.make_pose(x, y, h)
        ok = self.send_arm_goal(pick_pose, label=f"pick {sq}")
        if not ok:
            self.get_logger().error(
                f"Arm failed to reach pick pose for {sq}; aborting")
            return
        time.sleep(0.1)

        # Open gripper
        self.get_logger().info("Open gripper")
        ok = self.send_gripper_goal(close=False, effort=0.0)  # open gripper
        if not ok:
            self.get_logger().error("Gripper failed to open")
        time.sleep(0.1)

    def send_gripper_goal(self, close: bool, effort: float = 0.0, timeout_sec: float = 3.0):
        if not self.gripper_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("Gripper action server not available")
            return

        goal_msg = GripperCommand.Goal()
        goal_msg.close = close          # True = close, False = open
        goal_msg.effort = effort        # 0.0 means "ignore effort" in your bridge

        self.get_logger().info(
            f"Sending gripper goal: close={close}, effort={effort:.3f}"
        )

        done_event = threading.Event()
        result_container = {}

        def _result_cb(result_future):
            try:
                result_msg = result_future.result().result
                result_container["result"] = result_msg
                self.get_logger().info(
                    f"[GRIPPER] Finished: success={result_msg.success}, "
                    f"message='{result_msg.message}'"
                )
            except Exception as e:
                self.get_logger().error(
                    f"[GRIPPER] Result retrieval failed: {e}"
                )
                result_container["error"] = e
            finally:
                done_event.set()

        def _goal_response_cb(goal_future):
            try:
                goal_handle = goal_future.result()
            except Exception as e:
                self.get_logger().error(
                    f"[GRIPPER] Goal send failed: {e}"
                )
                result_container["error"] = e
                done_event.set()
                return

            if not goal_handle.accepted:
                self.get_logger().warn(
                    "[GRIPPER] Goal was rejected by server"
                )
                result_container["rejected"] = True
                done_event.set()
                return

            self.get_logger().info("[GRIPPER] Goal accepted")
            # now wait for result
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(_result_cb)

        # Send goal asynchronously; we get a Future for the goal handle
        send_future = self.gripper_client.send_goal_async(
            goal_msg,
            feedback_callback=self._gripper_feedback_cb
        )
        send_future.add_done_callback(_goal_response_cb)

        # Block current thread until result or timeout
        if not done_event.wait(timeout_sec):
            self.get_logger().error(
                "[GRIPPER] Timeout waiting for result"
            )
            return False

        if "result" in result_container:
            return bool(result_container["result"].success)

        # any other path -> failure
        return False

    def _gripper_feedback_cb(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f"Gripper feedback: {fb.progress_percent:.1f}% — {fb.stage}"
        )

    def send_arm_goal(self, pose: PoseStamped, label: str = "",
                      timeout_sec: float = 30.0) -> bool:
        """Send an arm MoveTCP goal and block until result (or timeout)."""
        if not self.arm_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("Arm action server 'arm/pick_place' not available")
            return False

        goal_msg = MoveTCP.Goal()
        goal_msg.pick_pose = pose

        tag = f" [{label}]" if label else ""
        self.get_logger().info(
            f"[ARM]{tag} Sending MoveTCP goal at "
            f"({pose.pose.position.x:.3f}, {pose.pose.position.y:.3f}, {pose.pose.position.z:.3f})"
        )

        done_event = threading.Event()
        result_container = {}

        def _result_cb(result_future):
            try:
                result_msg = result_future.result().result
                result_container["result"] = result_msg
                self.get_logger().info(
                    f"[ARM]{tag} Finished: success={result_msg.success}, "
                    f"message='{result_msg.message}'"
                )
            except Exception as e:
                self.get_logger().error(
                    f"[ARM]{tag} Result retrieval failed: {e}")
                result_container["error"] = e
            finally:
                done_event.set()

        def _goal_response_cb(goal_future):
            try:
                goal_handle = goal_future.result()
            except Exception as e:
                self.get_logger().error(f"[ARM]{tag} Goal send failed: {e}")
                result_container["error"] = e
                done_event.set()
                return

            if not goal_handle.accepted:
                self.get_logger().warn(f"[ARM]{tag} Goal was rejected")
                result_container["rejected"] = True
                done_event.set()
                return

            self.get_logger().info(f"[ARM]{tag} Goal accepted")
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(_result_cb)

        send_future = self.arm_client.send_goal_async(
            goal_msg,
            feedback_callback=self._arm_feedback_cb
        )
        send_future.add_done_callback(_goal_response_cb)

        if not done_event.wait(timeout_sec):
            self.get_logger().error(f"[ARM]{tag} Timeout waiting for result")
            return False

        if "result" in result_container:
            return bool(result_container["result"].success)

        return False

    def _arm_feedback_cb(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f"[ARM] Feedback: {fb.progress_percent:.1f}% — {fb.stage}"
        )

    def make_pose(self, x: float, y: float, z: float) -> PoseStamped:
        pose = PoseStamped()
        pose.header.frame_id = "base_link"   # or "base_link" – match your arm controller
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x / 1000.0
        pose.pose.position.y = y / 1000.0
        pose.pose.position.z = z / 1000.0

        # simple upright orientation; adjust if your MoveTCP expects something else
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = 0.0
        pose.pose.orientation.w = 1.0

        return pose


def main(args=None):
    rclpy.init(args=args)
    node = TaskCoordinator()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
