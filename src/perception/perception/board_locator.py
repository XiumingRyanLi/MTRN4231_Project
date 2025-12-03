#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np
import json


class ChessboardBorderDetector(Node):
    def __init__(self):
        super().__init__('chessboard_border_detector')
        
        # Create CV Bridge
        self.bridge = CvBridge()
        
        # Subscribe to camera topic
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10)
        
        # Publishers for debugging visualization
        self.pub_final = self.create_publisher(Image, '/chessboard/final_detection', 10)
        self.pub_gray = self.create_publisher(Image, '/chessboard/debug/gray', 10)
        self.pub_thresh = self.create_publisher(Image, '/chessboard/debug/threshold', 10)
        self.pub_morph = self.create_publisher(Image, '/chessboard/debug/morphology', 10)
        self.pub_contours = self.create_publisher(Image, '/chessboard/debug/contours', 10)
        
        # Publisher for cropped board image
        self.pub_crop = self.create_publisher(Image, '/board_crop', 10)
        
        # Publisher for board corners
        self.pub_corners = self.create_publisher(String, '/chess/board_corners', 10)
        
        self.get_logger().info('Chessboard border detector node started')
        self.get_logger().info('Publishing debug topics:')
        self.get_logger().info('  - /chessboard/debug/gray')
        self.get_logger().info('  - /chessboard/debug/threshold')
        self.get_logger().info('  - /chessboard/debug/morphology')
        self.get_logger().info('  - /chessboard/debug/contours')
        self.get_logger().info('  - /chessboard/final_detection')
        self.get_logger().info('  - /chess/board_corners')
        self.get_logger().info('  - /board_crop')
    
    def detect_white_border_corners(self, image):
        """
        Detect the four corners of the white border around the chessboard
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.get_logger().debug('Converted to grayscale')
        
        # Publish grayscale for debugging
        gray_msg = self.bridge.cv2_to_imgmsg(gray, encoding='mono8')
        self.pub_gray.publish(gray_msg)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Threshold to isolate white border
        # Adjust threshold values based on lighting conditions
        _, thresh = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY)
        self.get_logger().debug(f'Applied threshold, white pixels: {np.count_nonzero(thresh)}')
        
        # Publish threshold image
        thresh_msg = self.bridge.cv2_to_imgmsg(thresh, encoding='mono8')
        self.pub_thresh.publish(thresh_msg)
        
        # Morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        self.get_logger().debug(f'After morphology, white pixels: {np.count_nonzero(thresh)}')
        
        # Publish morphology result
        morph_msg = self.bridge.cv2_to_imgmsg(thresh, encoding='mono8')
        self.pub_morph.publish(morph_msg)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.get_logger().info(f'Found {len(contours)} contours')
        
        # Draw all contours for debugging
        contour_debug = image.copy()
        cv2.drawContours(contour_debug, contours, -1, (0, 255, 0), 2)
        contour_msg = self.bridge.cv2_to_imgmsg(contour_debug, encoding='bgr8')
        self.pub_contours.publish(contour_msg)
        
        if not contours:
            self.get_logger().warn('No contours found!')
            return None, None, image
        
        # Sort contours by area and show top 5
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for i, cnt in enumerate(sorted_contours[:5]):
            area = cv2.contourArea(cnt)
            self.get_logger().info(f'  Contour {i+1}: area = {area:.0f} pixels')
        
        # Find the largest contour (assuming it's the white border)
        largest_contour = sorted_contours[0]
        largest_area = cv2.contourArea(largest_contour)
        self.get_logger().info(f'Using largest contour with area: {largest_area:.0f} pixels')
        
        # Get the bounding rectangle
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        
        self.get_logger().info(f'Polygon approximation found {len(approx)} points')
        
        # If we have 4 points, we found the corners
        if len(approx) == 4:
            corners = approx.reshape(4, 2)
            
            # Sort corners: top-left, top-right, bottom-right, bottom-left
            corners = self.order_corners(corners)
            
            # Calculate indented corners (20 pixels inward)
            indented_corners = self.indent_corners(corners, 90)
            
            # Draw on output image
            output = image.copy()
            
            # Draw outer contour (white border)
            cv2.drawContours(output, [approx], 0, (0, 255, 0), 3)
            
            # Draw outer corners
            for i, corner in enumerate(corners):
                cv2.circle(output, tuple(corner), 10, (0, 0, 255), -1)
                cv2.putText(output, f'C{i+1}', tuple(corner + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Draw inner square (indented border)
            inner_contour = indented_corners.reshape((-1, 1, 2))
            cv2.drawContours(output, [inner_contour], 0, (255, 0, 0), 2)
            
            # Draw inner corners with chess notation
            chess_labels = ['H1', 'A1', 'A8', 'H8']
            for i, (corner, label) in enumerate(zip(indented_corners, chess_labels)):
                cv2.circle(output, tuple(corner), 8, (255, 0, 255), -1)
                cv2.putText(output, label, tuple(corner - np.array([10, 20])), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            self.get_logger().info('✓ Successfully detected 4 corners!')
            return corners, indented_corners, output
        else:
            self.get_logger().warn(f'Polygon has {len(approx)} points, need exactly 4')
            # Draw the approximation anyway for debugging
            output = image.copy()
            cv2.drawContours(output, [approx], 0, (0, 255, 255), 3)
            for point in approx:
                pt = tuple(point[0])
                cv2.circle(output, pt, 8, (255, 0, 255), -1)
            return None, None, output
    
    def order_corners(self, corners):
        """
        Order corners as: top-left, top-right, bottom-right, bottom-left
        """
        # Sort by y-coordinate
        sorted_by_y = corners[np.argsort(corners[:, 1])]
        
        # Top two points
        top = sorted_by_y[:2]
        top = top[np.argsort(top[:, 0])]  # Sort by x
        
        # Bottom two points
        bottom = sorted_by_y[2:]
        bottom = bottom[np.argsort(bottom[:, 0])]  # Sort by x
        
        return np.array([top[0], top[1], bottom[1], bottom[0]], dtype=np.int32)
        
    def indent_corners(self, corners, indent_pixels):
        """
        Indent corners inward by specified number of pixels.
        Works correctly even when the quadrilateral is rotated.
        Corners order: top-left, top-right, bottom-right, bottom-left
        Returns corners in order: A8 (top-left), H8 (top-right), H1 (bottom-right), A1 (bottom-left)
        """
        indented = np.zeros_like(corners, dtype=np.float64)
        
        for i in range(4):
            # Get the two edges adjacent to this corner
            prev_idx = (i - 1) % 4
            next_idx = (i + 1) % 4
            
            # Calculate edge vectors
            edge1 = corners[i] - corners[prev_idx]  # Edge coming into this corner
            edge2 = corners[next_idx] - corners[i]  # Edge going out of this corner
            
            # Normalize the edges
            edge1_len = np.linalg.norm(edge1)
            edge2_len = np.linalg.norm(edge2)
            
            if edge1_len > 0:
                edge1_unit = edge1 / edge1_len
            else:
                edge1_unit = np.array([0.0, 0.0])
                
            if edge2_len > 0:
                edge2_unit = edge2 / edge2_len
            else:
                edge2_unit = np.array([0.0, 0.0])
            
            # Get perpendicular inward normals (rotate 90° clockwise for inward direction)
            # For a vector [x, y], rotating 90° clockwise gives [y, -x]
            normal1 = np.array([edge1_unit[1], -edge1_unit[0]])
            normal2 = np.array([edge2_unit[1], -edge2_unit[0]])
            
            # Average the two normals to get the bisector direction
            bisector = normal1 + normal2
            bisector_len = np.linalg.norm(bisector)
            
            if bisector_len > 0:
                bisector_unit = bisector / bisector_len
            else:
                bisector_unit = np.array([0.0, 0.0])
            
            # Calculate how much to move along the bisector
            # The indent distance needs to be adjusted based on the angle between edges
            angle = np.arccos(np.clip(np.dot(edge1_unit, edge2_unit), -1.0, 1.0))
            
            # Avoid division by zero for very small angles
            if abs(np.sin(angle / 2)) > 1e-6:
                move_distance = indent_pixels / np.sin(angle / 2)
            else:
                move_distance = indent_pixels
            
            # Move the corner inward
            indented[i] = corners[i] + bisector_unit * move_distance
        
        return indented
        
    def crop_and_warp_board(self, image, corners):
        """
        Crop and perspective-transform the board to a square image.
        Corners should be in order: top-left, top-right, bottom-right, bottom-left
        """
        # Calculate the width and height of the board
        width_top = np.linalg.norm(corners[1] - corners[0])
        width_bottom = np.linalg.norm(corners[2] - corners[3])
        max_width = int(max(width_top, width_bottom))
        
        height_left = np.linalg.norm(corners[3] - corners[0])
        height_right = np.linalg.norm(corners[2] - corners[1])
        max_height = int(max(height_left, height_right))
        
        # Use square dimensions (largest side)
        output_size = max(max_width, max_height)
        
        # Define destination points for the warped image (square)
        dst_points = np.array([
            [0, 0],
            [output_size - 1, 0],
            [output_size - 1, output_size - 1],
            [0, output_size - 1]
        ], dtype=np.float32)
        
        # Get perspective transform matrix
        src_points = corners.astype(np.float32)
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        
        # Warp the image
        warped = cv2.warpPerspective(image, matrix, (output_size, output_size))
        
        return warped
    
    def publish_corners(self, corners):
        """
        Publish corners as a dictionary with chess notation.
        Corners order: A8 (top-left), H8 (top-right), H1 (bottom-right), A1 (bottom-left)
        """
        corners_dict = {
            'H1': [int(corners[0][0]), int(corners[0][1])],
            'A1': [int(corners[1][0]), int(corners[1][1])],
            'A8': [int(corners[2][0]), int(corners[2][1])],
            'H8': [int(corners[3][0]), int(corners[3][1])]
        }
        
        # Convert to JSON string and publish
        msg = String()
        msg.data = json.dumps(corners_dict)
        self.pub_corners.publish(msg)
    
    def image_callback(self, msg):
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Detect corners
            outer_corners, inner_corners, output_image = self.detect_white_border_corners(cv_image)
            
            if outer_corners is not None:
                self.get_logger().info('═══════════════════════════════')
                self.get_logger().info('CORNER DETECTION SUCCESSFUL')
                
                # Log corner positions
                chess_labels = ['H1', 'A1', 'A8', 'H8']
                for i, (corner, label) in enumerate(zip(inner_corners, chess_labels)):
                    self.get_logger().info(f'  {label}: x={corner[0]:4d}, y={corner[1]:4d}')
                self.get_logger().info('═══════════════════════════════')
                
                # Publish corners to topic
                self.publish_corners(inner_corners)
                
                # Crop and warp the board using outer corners
                cropped_board = self.crop_and_warp_board(cv_image, outer_corners)
                
                # Publish cropped board
                crop_msg = self.bridge.cv2_to_imgmsg(cropped_board, encoding='bgr8')
                self.pub_crop.publish(crop_msg)
                self.get_logger().info(f'Published cropped board: {cropped_board.shape[0]}x{cropped_board.shape[1]}')
                
            else:
                self.get_logger().warn('═══════════════════════════════')
                self.get_logger().warn('FAILED TO DETECT 4 CORNERS')
                self.get_logger().warn('Check debug topics for details')
                self.get_logger().warn('Not publishing to /chess/board_corners or /board_crop')
                self.get_logger().warn('═══════════════════════════════')
            
            # Publish final visualization
            output_msg = self.bridge.cv2_to_imgmsg(output_image, encoding='bgr8')
            self.pub_final.publish(output_msg)
            
        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    node = ChessboardBorderDetector()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()