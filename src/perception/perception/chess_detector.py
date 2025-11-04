#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String, Empty
from cv_bridge import CvBridge
import cv2
import numpy as np
import math
import json

class ChessBoardDetectorNode(Node):
    def __init__(self):
        super().__init__('chess_board_detector_node')
        
        # Parameters
        self.declare_parameter('image_topic', '/camera/camera/color/image_raw')
        self.declare_parameter('publish_debug_images', True)
        self.declare_parameter('square_threshold', 35)
        
        # Get parameters
        image_topic = self.get_parameter('image_topic').value
        self.publish_debug = self.get_parameter('publish_debug_images').value
        self.square_threshold = self.get_parameter('square_threshold').value
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # State variables
        self.latest_image = None
        self.coord_dict = None
        self.M_inv = None
        self.previous_occupancy = None
        
        # Subscribers
        self.image_sub = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )
        
        self.trigger_sub = self.create_subscription(
            Empty,
            '/take_picture',
            self.trigger_callback,
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
        
        self.get_logger().info('Chess Board Detector Node initialized')
        self.get_logger().info(f'Listening to: {image_topic}')
        self.get_logger().info('Waiting for trigger on /take_picture')

    def image_callback(self, msg):
        """Store the latest image without processing"""
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Error converting image: {str(e)}')

    def trigger_callback(self, msg):
        """Process the latest image when triggered"""
        if self.latest_image is None:
            self.get_logger().warn('Trigger received but no image available yet')
            return
        
        self.get_logger().info('Processing triggered image...')
        self.process_latest_image()

    def process_latest_image(self):
        """Process the stored latest image"""
        try:
            cv_image = self.latest_image
            
            # Process the image
            success, coord_dict, warped_image, debug_image, M_inv = self.process_chessboard(cv_image)
            
            if success:
                # Store transformation matrix and coordinates
                self.coord_dict = coord_dict
                self.M_inv = M_inv
                
                # Detect pieces
                occupancy_dict = self.detect_pieces(cv_image, coord_dict)
                
                # Publish occupancy
                self.publish_occupancy(occupancy_dict)
                
                # Publish coordinates
                self.publish_coordinates(coord_dict)
                
                # Detect move if we have previous state
                if self.previous_occupancy is not None:
                    move_info = self.detect_move(self.previous_occupancy, occupancy_dict)
                    if move_info and 'from_square' in move_info:
                        capture_text = " (capture)" if move_info['is_capture'] else ""
                        self.get_logger().info(
                            f"Move: {move_info['piece_color']} from {move_info['from_square']} "
                            f"to {move_info['to_square']}{capture_text}"
                        )
                
                self.previous_occupancy = occupancy_dict
                
                # Publish debug images
                if self.publish_debug:
                    if debug_image is not None:
                        debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding='bgr8')
                        self.debug_image_pub.publish(debug_msg)
                    
                    if warped_image is not None:
                        warped_msg = self.bridge.cv2_to_imgmsg(warped_image, encoding='rgb8')
                        self.warped_image_pub.publish(warped_msg)
                        
            else:
                self.get_logger().warn('Failed to detect chessboard')
                
        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')

    def process_chessboard(self, image):
        """Process image to extract chessboard"""
        try:
            # Convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Threshold
            ret, otsu_binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
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
                        cv2.line(black_image, (x1, y1), (x2, y2), (255, 255, 255), 2)
            
            kernel = np.ones((15, 15), np.uint8)
            black_image = cv2.morphologyEx(black_image, cv2.MORPH_CLOSE, kernel)
            
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
                        index_sorted = sorted(pts, key=lambda x: x[0], reverse=True)
                        
                        if index_sorted[0][1] < index_sorted[1][1]:
                            index_sorted[0], index_sorted[1] = index_sorted[1], index_sorted[0]
                        
                        if index_sorted[2][1] > index_sorted[3][1]:
                            index_sorted[2], index_sorted[3] = index_sorted[3], index_sorted[2]
                        
                        pt1, pt2, pt3, pt4 = index_sorted
                        
                        l1 = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
                        l2 = math.sqrt((pt2[0] - pt3[0])**2 + (pt2[1] - pt3[1])**2)
                        l3 = math.sqrt((pt3[0] - pt4[0])**2 + (pt3[1] - pt4[1])**2)
                        l4 = math.sqrt((pt1[0] - pt4[0])**2 + (pt1[1] - pt4[1])**2)
                        
                        lengths = [l1, l2, l3, l4]
                        max_length = max(lengths)
                        min_length = min(lengths)
                        
                        if (max_length - min_length) <= self.square_threshold:
                            cv2.line(valid_squares_image, tuple(pt1), tuple(pt2), (255, 255, 0), 7)
                            cv2.line(valid_squares_image, tuple(pt2), tuple(pt3), (255, 255, 0), 7)
                            cv2.line(valid_squares_image, tuple(pt3), tuple(pt4), (255, 255, 0), 7)
                            cv2.line(valid_squares_image, tuple(pt1), tuple(pt4), (255, 255, 0), 7)
            
            # Dilate valid squares
            kernel = np.ones((7, 7), np.uint8)
            dilated_valid_squares_image = cv2.dilate(valid_squares_image, kernel, iterations=1)
            
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
            extreme_points_list = np.float32([top_left, top_right, bottom_left, bottom_right])
            
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
                    bottom_left_sq = (j * square_width, (i + 1) * square_height)
                    bottom_right_sq = ((j + 1) * square_width, (i + 1) * square_height)
                    
                    x_center = (top_left_sq[0] + bottom_right_sq[0]) // 2
                    y_center = (top_left_sq[1] + bottom_right_sq[1]) // 2
                    
                    squares_data_warped.append([
                        (x_center, y_center),
                        bottom_right_sq,
                        top_right_sq,
                        top_left_sq,
                        bottom_left_sq
                    ])
            
            squares_data_warped_np = np.array(squares_data_warped, dtype=np.float32).reshape(-1, 1, 2)
            squares_data_original_np = cv2.perspectiveTransform(squares_data_warped_np, M_inv)
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

    def get_sample_region(self, center_x, center_y, radius=10):
        """Get sample points around center"""
        points = []
        for angle in range(0, 360, 30):
            rad = np.radians(angle)
            x = int(center_x + radius * np.cos(rad))
            y = int(center_y + radius * np.sin(rad))
            points.append((x, y))
        return points

    def detect_piece_color(self, image, cell_coords, piece_color_ranges):
        """Detect if piece is black, white, or empty"""
        center_x, center_y = self.get_cell_center(cell_coords)
        sample_points = self.get_sample_region(center_x, center_y)
        
        color_counts = {'black': 0, 'white': 0}
        total_points = len(sample_points)
        
        for x, y in sample_points:
            if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                pixel = image[y, x]
                
                for color_name, color_range in piece_color_ranges.items():
                    lower, upper = color_range
                    if np.all(pixel >= lower) and np.all(pixel <= upper):
                        color_counts[color_name] += 1
                        break
        
        threshold = total_points * 0.1
        
        if color_counts['black'] > threshold and color_counts['black'] > color_counts['white']:
            return 'black'
        elif color_counts['white'] > threshold and color_counts['white'] > color_counts['black']:
            return 'white'
        else:
            return 'empty'

    def detect_pieces(self, image, coord_dict):
        """Detect all pieces on the board"""
        piece_color_ranges = {
            'black': (np.array([0, 0, 0]), np.array([30, 30, 30])),
            'white': (np.array([150, 150, 120]), np.array([255, 255, 255]))
        }
        
        occupancy_dict = {}
        
        for cell_num, cell_coords in coord_dict.items():
            piece_color = self.detect_piece_color(image, cell_coords, piece_color_ranges)
            occupancy_dict[cell_num] = piece_color
        

        x, y = self.get_cell_center(coord_dict[46])
        samples = self.get_sample_region(x, y)

        for x, y in samples:
            pixel = image[y,x]
            self.get_logger().info(f'colour: {pixel}')

        #self.get_logger().info(f'Occupancy: {occupancy_dict[1]}')
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
            is_capture = occupancy_dict_before[to_squares[0]] in ['black', 'white']
            
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
        """Convert cell number (0-63) to algebraic notation (a1-h8)"""
        row = cell_num // 8
        col = cell_num % 8
        file = chr(ord('a') + col)  # Convert column to letter (a-h)
        rank = str(8 - row)  # Convert row to rank (8-1)
        return f"{file}{rank}"

    def publish_occupancy(self, occupancy_dict):
        """Publish occupancy dictionary as JSON string"""
        msg = String()
        msg.data = json.dumps(occupancy_dict)
        self.occupancy_pub.publish(msg)

    def publish_coordinates(self, coord_dict):
        """Publish board coordinates as JSON string"""
        msg = String()
        # Convert numpy types to native Python types for JSON serialization
        serializable_dict = {}
        for key, value in coord_dict.items():
            serializable_dict[str(key)] = [[int(coord[0]), int(coord[1])] for coord in value]
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