#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


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
        
        self.get_logger().info('Chessboard border detector node started')
        self.get_logger().info('Publishing debug topics:')
        self.get_logger().info('  - /chessboard/debug/gray')
        self.get_logger().info('  - /chessboard/debug/threshold')
        self.get_logger().info('  - /chessboard/debug/morphology')
        self.get_logger().info('  - /chessboard/debug/contours')
        self.get_logger().info('  - /chessboard/final_detection')
    
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
        _, thresh = cv2.threshold(blurred, 170, 255, cv2.THRESH_BINARY)
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
            return None, image
        
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
            
            # Draw on output image
            output = image.copy()
            
            # Draw contour
            cv2.drawContours(output, [approx], 0, (0, 255, 0), 3)
            
            # Draw corners
            for i, corner in enumerate(corners):
                cv2.circle(output, tuple(corner), 10, (0, 0, 255), -1)
                cv2.putText(output, f'C{i+1}', tuple(corner + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            self.get_logger().info('✓ Successfully detected 4 corners!')
            return corners, output
        else:
            self.get_logger().warn(f'Polygon has {len(approx)} points, need exactly 4')
            # Draw the approximation anyway for debugging
            output = image.copy()
            cv2.drawContours(output, [approx], 0, (0, 255, 255), 3)
            for point in approx:
                pt = tuple(point[0])
                cv2.circle(output, pt, 8, (255, 0, 255), -1)
            return None, output
    
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
    
    def image_callback(self, msg):
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Detect corners
            corners, output_image = self.detect_white_border_corners(cv_image)
            
            if corners is not None:
                self.get_logger().info('═══════════════════════════════')
                self.get_logger().info('CORNER DETECTION SUCCESSFUL')
                
                # Log corner positions
                for i, corner in enumerate(corners):
                    self.get_logger().info(f'  Corner {i+1}: x={corner[0]:4d}, y={corner[1]:4d}')
                self.get_logger().info('═══════════════════════════════')
            else:
                self.get_logger().warn('═══════════════════════════════')
                self.get_logger().warn('FAILED TO DETECT 4 CORNERS')
                self.get_logger().warn('Check debug topics for details')
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