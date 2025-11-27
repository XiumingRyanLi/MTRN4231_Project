#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String, Bool
from cv_bridge import CvBridge
import cv2
import numpy as np
import math
import json
from collections import deque


class ChessBoardDetectorNode(Node):
    def __init__(self):
        super().__init__('chess_board_detector_node')

        # Parameters
        self.declare_parameter('image_topic', '/camera/camera/color/image_raw')
        self.declare_parameter('publish_debug_images', True)
        self.declare_parameter('square_threshold', 35)
        self.declare_parameter('stability_duration', 1.0)  # seconds

        # Get parameters
        image_topic = self.get_parameter('image_topic').value
        self.publish_debug = self.get_parameter('publish_debug_images').value
        self.square_threshold = self.get_parameter('square_threshold').value
        self.stability_duration = self.get_parameter('stability_duration').value

        # CV Bridge
        self.bridge = CvBridge()

        # State variables
        self.coord_dict = None
        self.M_inv = None
        self.last_published_occupancy = None
        self.is_calibrated = False
        self.piece_color_ranges = None
        
        # Stability tracking
        self.occupancy_history = deque(maxlen=100)  # Store recent occupancy states
        self.last_stable_occupancy = None
        self.stable_start_time = None
        self.move_detected = False

        # Subscribers
        self.image_sub = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )

        self.trigger_sub = self.create_subscription(
            Bool,
            '/calibrate_colors',
            self.calibrate_callback,
            10
        )

        # Publishers
        self.occupancy_pub = self.create_publisher(
            String,
            '/chess/occupancy',
            10
        )

        self.board_coords_pub = self.create_publisher(
            String,
            '/chess/board_coordinates',
            10
        )

        if self.publish_debug:
            self.debug_image_pub = self.create_publisher(
                Image,
                '/chess/debug_image',
                10
            )

            self.warped_image_pub = self.create_publisher(
                Image,
                '/chess/warped_board',
                10
            )
            self.cropped_image_pub = self.create_publisher(
                Image,
                'chess/cropped_image',
                10
            )

        self.get_logger().info('Chess Board Detector Node initialized')
        self.get_logger().info(f'Listening to: {image_topic}')
        self.get_logger().info(f'Stability duration: {self.stability_duration}s')
        self.get_logger().info('Send trigger to /calibrate_colors to calibrate from initial position')

    def image_callback(self, msg):
        """Process each incoming frame"""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            # Image is already cropped by board_locator node
            cropped_image = cv_image
            
            if self.publish_debug:
                cropped_msg = self.bridge.cv2_to_imgmsg(
                    cropped_image, encoding='bgr8')
                self.cropped_image_pub.publish(cropped_msg)
            
            # Process the frame
            self.process_frame(cropped_image)
            
        except Exception as e:
            self.get_logger().error(f'Error converting image: {str(e)}')

    def calibrate_callback(self, msg):
        """Trigger color calibration from initial position"""
        if msg.data:
            self.get_logger().info('Calibration triggered - will calibrate on next successful board detection')
            self.is_calibrated = False

    def process_frame(self, image):
        """Process a single frame"""
        try:
            # Process the chessboard
            success, coord_dict, warped_image, debug_image, M_inv = self.process_chessboard(image)

            if not success:
                # Board detection failed, don't publish anything
                return

            # Store transformation matrix and coordinates
            self.coord_dict = coord_dict
            self.M_inv = M_inv

            # If not calibrated, try to calibrate from current position
            if not self.is_calibrated:
                calibration_success = self.calibrate_piece_colors(image, coord_dict)
                if not calibration_success:
                    self.get_logger().warn('Waiting for calibration...')
                    return
                # After calibration, set the initial state
                occupancy_dict = self.detect_pieces(image, coord_dict)
                self.last_published_occupancy = occupancy_dict
                self.last_stable_occupancy = occupancy_dict
                self.publish_state(occupancy_dict, coord_dict)
                self.get_logger().info('Initial board state published')
                return

            # Detect pieces
            occupancy_dict = self.detect_pieces(image, coord_dict)
            
            # Add to history with timestamp
            current_time = self.get_clock().now()
            self.occupancy_history.append((current_time, occupancy_dict))
            
            # Check if occupancy is stable
            is_stable, stable_occupancy = self.check_stability()
            
            if is_stable:
                # Check if this is different from last published state
                if self.last_published_occupancy is None:
                    # First stable state
                    self.publish_state(stable_occupancy, coord_dict)
                    self.last_published_occupancy = stable_occupancy
                    self.move_detected = False
                elif self.occupancies_different(self.last_published_occupancy, stable_occupancy):
                    # Move detected
                    if not self.move_detected:
                        self.move_detected = True
                        self.stable_start_time = current_time
                        self.last_stable_occupancy = stable_occupancy
                        move_info = self.detect_move(self.last_published_occupancy, stable_occupancy)
                        if move_info and 'from_square' in move_info:
                            capture_text = " (capture)" if move_info['is_capture'] else ""
                            self.get_logger().info(
                                f"Move detected: {move_info['piece_color']} from {move_info['from_square']} "
                                f"to {move_info['to_square']}{capture_text} - waiting for stability..."
                            )
                    else:
                        # Check if still the same stable state
                        if self.occupancies_same(self.last_stable_occupancy, stable_occupancy):
                            # Check if stable for required duration
                            time_stable = (current_time - self.stable_start_time).nanoseconds / 1e9
                            if time_stable >= self.stability_duration:
                                # Publish the new state
                                self.publish_state(stable_occupancy, coord_dict)
                                self.last_published_occupancy = stable_occupancy
                                self.move_detected = False
                                self.get_logger().info(f'New game state published after {time_stable:.2f}s stability')
                        else:
                            # State changed again, reset timer
                            self.stable_start_time = current_time
                            self.last_stable_occupancy = stable_occupancy

            # Publish debug images
            if self.publish_debug:
                if debug_image is not None:
                    debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding='bgr8')
                    self.debug_image_pub.publish(debug_msg)

                if warped_image is not None:
                    warped_msg = self.bridge.cv2_to_imgmsg(warped_image, encoding='rgb8')
                    self.warped_image_pub.publish(warped_msg)

        except Exception as e:
            self.get_logger().error(f'Error processing frame: {str(e)}')

    def check_stability(self):
        """Check if occupancy has been stable for the required duration"""
        if len(self.occupancy_history) < 2:
            return False, None
        
        current_time = self.get_clock().now()
        cutoff_time = current_time - rclpy.duration.Duration(seconds=self.stability_duration)
        
        # Get all states within the stability window
        recent_states = [
            (t, occ) for t, occ in self.occupancy_history 
            if t >= cutoff_time
        ]
        
        if not recent_states:
            return False, None
        
        # Check if all recent states are the same
        first_occupancy = recent_states[0][1]
        for _, occupancy in recent_states[1:]:
            if not self.occupancies_same(first_occupancy, occupancy):
                return False, None
        
        return True, first_occupancy

    def occupancies_same(self, occ1, occ2):
        """Check if two occupancy dictionaries are the same"""
        if occ1 is None or occ2 is None:
            return False
        if set(occ1.keys()) != set(occ2.keys()):
            return False
        for key in occ1.keys():
            if occ1[key] != occ2[key]:
                return False
        return True

    def occupancies_different(self, occ1, occ2):
        """Check if two occupancy dictionaries are different"""
        return not self.occupancies_same(occ1, occ2)

    def publish_state(self, occupancy_dict, coord_dict):
        """Publish occupancy and coordinates"""
        self.publish_occupancy(occupancy_dict)
        self.publish_coordinates(coord_dict)

    def calibrate_piece_colors(self, image, coord_dict):
        """Automatically calibrate piece colors from initial board position"""
        self.get_logger().info('Starting automatic color calibration...')
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Cells 1-16 should have black pieces (rows 1-2)
        black_cells = list(range(1, 17))
        # Cells 49-64 should have white pieces (rows 7-8)
        white_cells = list(range(49, 65))

        # Collect samples from black pieces
        black_samples = []
        for cell_num in black_cells:
            if cell_num in coord_dict:
                cell_coords = coord_dict[cell_num]
                center_x, center_y = self.get_cell_center(cell_coords)
                sample_points = self.get_sample_region(center_x, center_y)

                for x, y in sample_points:
                    if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                        pixel = image[y, x]
                        black_samples.append(pixel.tolist())

        # Collect samples from white pieces
        white_samples = []
        for cell_num in white_cells:
            if cell_num in coord_dict:
                cell_coords = coord_dict[cell_num]
                center_x, center_y = self.get_cell_center(cell_coords)
                sample_points = self.get_sample_region(center_x, center_y)

                for x, y in sample_points:
                    if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                        pixel = image[y, x]
                        white_samples.append(pixel.tolist())

        if not black_samples or not white_samples:
            self.get_logger().error('Failed to collect calibration samples')
            return False
        
        # x, y = self.get_cell_center(coord_dict[17])
        # sample_points = self.get_sample_region(x, y)
        # self.get_logger().info(sample_points)

        # Convert to numpy arrays for easier processing
        black_samples = np.array(black_samples)
        white_samples = np.array(white_samples)

        # Sort samples by brightness (sum of BGR values) to identify outliers
        black_brightness = np.sum(black_samples, axis=1)
        white_brightness = np.sum(white_samples, axis=1)

        # Remove top 2 and bottom 2 outliers for black pieces
        black_sorted_indices = np.argsort(black_brightness)
        if len(black_sorted_indices) > 4:
            k = len(black_sorted_indices) // 7
            black_filtered_indices = black_sorted_indices[2:-k]
            black_filtered = black_samples[black_filtered_indices]
        else:
            black_filtered = black_samples

        # Remove top 2 and bottom 2 outliers for white pieces
        white_sorted_indices = np.argsort(white_brightness)
        if len(white_sorted_indices) > 4:
            w = len(white_sorted_indices) // 10
            white_filtered_indices = white_sorted_indices[w:-2]
            white_filtered = white_samples[white_filtered_indices]
        else:
            white_filtered = white_samples

        # Calculate bounds for black pieces
        # Lower bound stays at [0, 0, 0]
        # Upper bound is the maximum from filtered samples, with some margin
        black_upper = np.percentile(black_filtered, 95, axis=0)  # 95th percentile
        # Add 15 margin, cap at 255
        black_upper = np.minimum(black_upper + 15, 255).astype(int)

        # Calculate bounds for white pieces
        # Upper bound stays at [255, 255, 255]
        # Lower bound is the minimum from filtered samples, with some margin
        white_lower = np.percentile(white_filtered, 5, axis=0)   # 5th percentile
        # Subtract 15 margin, floor at 0
        white_lower = np.maximum(white_lower - 15, 0).astype(int)

        # Store calibrated ranges
        self.piece_color_ranges = {
            'black': (np.array([0, 0, 0]), np.array(black_upper)),
            'white': (np.array(white_lower), np.array([255, 255, 255]))
        }

        self.get_logger().info(
            f'Black piece range calibrated: [0, 0, 0] to {black_upper.tolist()}')
        self.get_logger().info(
            f'White piece range calibrated: {white_lower.tolist()} to [255, 255, 255]')
        self.get_logger().info(
            f'Analyzed {len(black_filtered)} black samples and {len(white_filtered)} white samples')

        self.is_calibrated = True
        return True

    def process_chessboard(self, image):
        """Process image to extract chessboard"""
        try:
            # Convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Threshold
            ret, otsu_binary = cv2.threshold(
                gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Canny edge detection
            canny_image = cv2.Canny(otsu_binary, 20, 255)

            # Dilation
            kernel = np.ones((7, 7), np.uint8)
            dilation_image = cv2.dilate(canny_image, kernel, iterations=1)

            # Hough Lines
            lines = cv2.HoughLinesP(dilation_image, 1, np.pi / 180, threshold=200,
                                    minLineLength=50, maxLineGap=100)

            # Create black image for lines
            black_image = np.zeros_like(dilation_image)

            # Draw filtered lines
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)

                    if angle < 10 or angle > 170 or (80 < angle < 100):
                        cv2.line(black_image, (x1, y1),
                                 (x2, y2), (255, 255, 255), 2)

            kernel = np.ones((15, 15), np.uint8)
            black_image = cv2.morphologyEx(
                black_image, cv2.MORPH_CLOSE, kernel)

            # Dilation
            kernel = np.ones((3, 3), np.uint8)
            black_image = cv2.dilate(black_image, kernel, iterations=1)

            # Find contours and filter squares
            board_contours, hierarchy = cv2.findContours(black_image, cv2.RETR_TREE,
                                                         cv2.CHAIN_APPROX_SIMPLE)

            valid_squares_image = np.zeros_like(black_image)

            for contour in board_contours:
                if 2000 < cv2.contourArea(contour) < 20000:
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)

                    if len(approx) == 4:
                        pts = [pt[0].tolist() for pt in approx]
                        index_sorted = sorted(
                            pts, key=lambda x: x[0], reverse=True)

                        if index_sorted[0][1] < index_sorted[1][1]:
                            index_sorted[0], index_sorted[1] = index_sorted[1], index_sorted[0]

                        if index_sorted[2][1] > index_sorted[3][1]:
                            index_sorted[2], index_sorted[3] = index_sorted[3], index_sorted[2]

                        pt1, pt2, pt3, pt4 = index_sorted

                        l1 = math.sqrt((pt1[0] - pt2[0]) **
                                       2 + (pt1[1] - pt2[1])**2)
                        l2 = math.sqrt((pt2[0] - pt3[0]) **
                                       2 + (pt2[1] - pt3[1])**2)
                        l3 = math.sqrt((pt3[0] - pt4[0]) **
                                       2 + (pt3[1] - pt4[1])**2)
                        l4 = math.sqrt((pt1[0] - pt4[0]) **
                                       2 + (pt1[1] - pt4[1])**2)

                        lengths = [l1, l2, l3, l4]
                        max_length = max(lengths)
                        min_length = min(lengths)

                        if (max_length - min_length) <= self.square_threshold:
                            cv2.line(valid_squares_image, tuple(
                                pt1), tuple(pt2), (255, 255, 0), 7)
                            cv2.line(valid_squares_image, tuple(
                                pt2), tuple(pt3), (255, 255, 0), 7)
                            cv2.line(valid_squares_image, tuple(
                                pt3), tuple(pt4), (255, 255, 0), 7)
                            cv2.line(valid_squares_image, tuple(
                                pt1), tuple(pt4), (255, 255, 0), 7)

            # Dilate valid squares
            kernel = np.ones((7, 7), np.uint8)
            dilated_valid_squares_image = cv2.dilate(
                valid_squares_image, kernel, iterations=1)

            # Find largest contour
            contours, _ = cv2.findContours(dilated_valid_squares_image, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

            if not contours:
                return False, None, None, None, None

            largest_contour = max(contours, key=cv2.contourArea)

            # Find extreme points
            top_left = None
            top_right = None
            bottom_left = None
            bottom_right = None

            for point in largest_contour[:, 0]:
                x, y = point

                if top_left is None or (x + y < top_left[0] + top_left[1]):
                    top_left = (x, y)
                if top_right is None or (x - y > top_right[0] - top_right[1]):
                    top_right = (x, y)
                if bottom_left is None or (x - y < bottom_left[0] - bottom_left[1]):
                    bottom_left = (x, y)
                if bottom_right is None or (x + y > bottom_right[0] + bottom_right[1]):
                    bottom_right = (x, y)

            # Perspective transform
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            extreme_points_list = np.float32(
                [top_left, top_right, bottom_left, bottom_right])

            threshold = 0
            width, height = 1200, 1200

            dst_pts = np.float32([
                [threshold, threshold],
                [width + threshold, threshold],
                [threshold, height + threshold],
                [width + threshold, height + threshold]
            ])

            M = cv2.getPerspectiveTransform(extreme_points_list, dst_pts)
            warped_image = cv2.warpPerspective(rgb_image, M,
                                               (width + 2 * threshold, height + 2 * threshold))

            # Calculate inverse matrix
            M_inv = cv2.invert(M)[1]

            # Divide into 64 squares
            rows, cols = 8, 8
            square_width = width // cols
            square_height = height // rows

            squares_data_warped = []

            for i in range(rows - 1, -1, -1):
                for j in range(cols):
                    top_left_sq = (j * square_width, i * square_height)
                    top_right_sq = ((j + 1) * square_width, i * square_height)
                    bottom_left_sq = (j * square_width,
                                      (i + 1) * square_height)
                    bottom_right_sq = ((j + 1) * square_width,
                                       (i + 1) * square_height)

                    x_center = (top_left_sq[0] + bottom_right_sq[0]) // 2
                    y_center = (top_left_sq[1] + bottom_right_sq[1]) // 2

                    squares_data_warped.append([
                        (x_center, y_center),
                        bottom_right_sq,
                        top_right_sq,
                        top_left_sq,
                        bottom_left_sq
                    ])

            squares_data_warped_np = np.array(
                squares_data_warped, dtype=np.float32).reshape(-1, 1, 2)
            squares_data_original_np = cv2.perspectiveTransform(
                squares_data_warped_np, M_inv)
            squares_data_original = squares_data_original_np.reshape(-1, 5, 2)

            # Create coordinate dictionary
            coord_dict = {}
            for idx, square in enumerate(squares_data_original):
                cell = idx + 1
                bottom_right = tuple(map(int, square[1]))
                top_right = tuple(map(int, square[2]))
                top_left = tuple(map(int, square[3]))
                bottom_left = tuple(map(int, square[4]))

                coord_dict[cell] = [
                    [bottom_right[0], bottom_right[1]],
                    [top_right[0], top_right[1]],
                    [top_left[0], top_left[1]],
                    [bottom_left[0], bottom_left[1]]
                ]

            # Create debug image
            debug_image = image.copy()
            for square in squares_data_original:
                pts = square[1:].astype(np.int32)
                cv2.polylines(debug_image, [pts], True, (0, 255, 0), 2)

            return True, coord_dict, warped_image, debug_image, M_inv

        except Exception as e:
            self.get_logger().error(f'Error in process_chessboard: {str(e)}')
            return False, None, None, None, None

    def get_cell_center(self, cell_coords):
        """Calculate center of cell"""
        x_coords = [coord[0] for coord in cell_coords]
        y_coords = [coord[1] for coord in cell_coords]
        center_x = int(np.mean(x_coords))
        center_y = int(np.mean(y_coords))
        return center_x, center_y

    def get_sample_region(self, center_x, center_y, radius=7):
        """Get sample points around center"""
        points = []
        for angle in range(0, 360, 30):
            rad = np.radians(angle)
            x = int(center_x + radius * np.cos(rad))
            y = int(center_y + radius * np.sin(rad))
            points.append((x, y))
        return points

    def detect_piece_color(self, image, cell_coords):
        """Detect if piece is black, white, or empty"""
        if self.piece_color_ranges is None:
            return 'empty'

        center_x, center_y = self.get_cell_center(cell_coords)
        sample_points = self.get_sample_region(center_x, center_y)

        color_counts = {'black': 0, 'white': 0}
        total_points = len(sample_points)

        for x, y in sample_points:
            if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                pixel = image[y, x]

                for color_name, color_range in self.piece_color_ranges.items():
                    lower, upper = color_range
                    if np.all(pixel >= lower) and np.all(pixel <= upper):
                        color_counts[color_name] += 1
                        break

        threshold = total_points * 0.2

        if color_counts['black'] > threshold and color_counts['black'] > color_counts['white']:
            return 'black'
        elif color_counts['white'] > threshold and color_counts['white'] > color_counts['black']:
            return 'white'
        else:
            return 'empty'

    def detect_pieces(self, image, coord_dict):
        """Detect all pieces on the board"""
        occupancy_dict = {}

        for cell_num, cell_coords in coord_dict.items():
            piece_color = self.detect_piece_color(image, cell_coords)
            occupancy_dict[cell_num] = piece_color

        return occupancy_dict

    def detect_move(self, occupancy_dict_before, occupancy_dict_after):
        """Detect moves between two board states"""
        from_squares = []
        to_squares = []

        for cell_num in occupancy_dict_before.keys():
            before = occupancy_dict_before[cell_num]
            after = occupancy_dict_after[cell_num]

            if before in ['black', 'white'] and after == 'empty':
                from_squares.append(cell_num)
            elif before == 'empty' and after in ['black', 'white']:
                to_squares.append(cell_num)
            elif before in ['black', 'white'] and after in ['black', 'white'] and before != after:
                to_squares.append(cell_num)

        if len(from_squares) == 1 and len(to_squares) == 1:
            is_capture = occupancy_dict_before[to_squares[0]] in [
                'black', 'white']

            # Convert cell numbers to algebraic notation
            from_algebraic = self.cell_to_algebraic(from_squares[0])
            to_algebraic = self.cell_to_algebraic(to_squares[0])

            return {
                'from_square': from_squares[0],
                'to_square': to_squares[0],
                'piece_color': occupancy_dict_after[to_squares[0]],
                'is_capture': is_capture,
                'move_notation': f"{from_algebraic}{to_algebraic}"
            }
        else:
            return {
                'from_squares': from_squares,
                'to_squares': to_squares,
                'note': 'Unexpected move pattern detected'
            }

    def cell_to_algebraic(self, cell_num):
        """Convert cell number (1-64) to algebraic notation (a1-h8)"""
        row = (cell_num - 1) // 8
        col = (cell_num - 1) % 8
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return f"{file}{rank}"

    def publish_occupancy(self, occupancy_dict):
        """Publish occupancy dictionary as JSON string"""
        msg = String()
        msg.data = json.dumps(occupancy_dict)
        self.occupancy_pub.publish(msg)

    def publish_coordinates(self, coord_dict):
        """Publish board coordinates as JSON string"""
        msg = String()
        serializable_dict = {}
        for key, value in coord_dict.items():
            serializable_dict[str(key)] = [
                [int(coord[0]), int(coord[1])] for coord in value]
        msg.data = json.dumps(serializable_dict)
        self.board_coords_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ChessBoardDetectorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()