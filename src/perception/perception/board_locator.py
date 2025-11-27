#!/usr/bin/env python3

import rclpy
import cv2
import tf2_ros
import numpy as np
import pyrealsense2 as rs
import json
from cv_bridge import CvBridge, CvBridgeError

from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PointStamped
from std_msgs.msg import String
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import tf2_geometry_msgs


class BoardLocatorNode(Node):
    def __init__(self):
        super().__init__('board_locator_node')
        
        # Parameters
        self.declare_parameter('board_height_offset', 0.1)  # 10cm above table
        self.declare_parameter('depth_threshold', 0.02)  # 2cm tolerance for plane detection
        self.declare_parameter('min_board_area', 0.1)  # Minimum board area in m^2
        self.declare_parameter('input_image_topic', '/camera/camera/color/image_raw')  # Input topic (should be remapped in launch to avoid loop)
        self.declare_parameter('output_image_topic', '/camera/camera/color/image_raw')  # Output topic
        
        self.board_height_offset = self.get_parameter('board_height_offset').value
        self.depth_threshold = self.get_parameter('depth_threshold').value
        self.min_board_area = self.get_parameter('min_board_area').value
        input_topic = self.get_parameter('input_image_topic').value
        output_topic = self.get_parameter('output_image_topic').value
        
        # CV Bridge
        self.cv_bridge = CvBridge()
        
        # Camera data
        self.intrinsics = None
        self.depth_image = None
        self.rgb_image = None
        
        # Board detection state
        self.board_corners_camera_frame = None
        self.board_detected = False
        self.last_published_stamp = None  # Track last published message to avoid feedback loop
        
        # Subscriptions
        self.image_sub = self.create_subscription(
            Image,
            input_topic,
            self.rgb_image_callback,
            10
        )
        
        self.depth_sub = self.create_subscription(
            Image,
            '/camera/camera/aligned_depth_to_color/image_raw',
            self.depth_image_callback,
            10
        )
        
        self.cam_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/camera/aligned_depth_to_color/camera_info',
            self.camera_info_callback,
            10
        )
        
        # Publishers
        self.cropped_image_pub = self.create_publisher(
            Image,
            output_topic,
            10
        )
        
        self.corners_pub = self.create_publisher(
            String,
            '/chess/board_corners',
            10
        )
        
        # TF2 setup
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Timer for processing
        self.processing_timer = self.create_timer(0.1, self.process_board_detection)
        
        self.get_logger().info('Board Locator Node initialized')
        self.get_logger().info(f'Looking for board at {self.board_height_offset}m above table')
        self.get_logger().info(f'Subscribing to: {input_topic}')
        self.get_logger().info(f'Publishing to: {output_topic}')
    
    def camera_info_callback(self, msg):
        """Store camera intrinsics from camera info"""
        try:
            if self.intrinsics:
                return
            
            self.intrinsics = rs.intrinsics()
            self.intrinsics.width = msg.width
            self.intrinsics.height = msg.height
            self.intrinsics.ppx = msg.k[2]
            self.intrinsics.ppy = msg.k[5]
            self.intrinsics.fx = msg.k[0]
            self.intrinsics.fy = msg.k[4]
            
            if msg.distortion_model == 'plumb_bob':
                self.intrinsics.model = rs.distortion.brown_conrady
            elif msg.distortion_model == 'equidistant':
                self.intrinsics.model = rs.distortion.kannala_brandt4
            
            self.intrinsics.coeffs = [float(i) for i in msg.d]
            
            self.get_logger().info('Camera intrinsics received')
        except Exception as e:
            self.get_logger().error(f'Error processing camera info: {str(e)}')
    
    def rgb_image_callback(self, msg):
        """Store RGB image"""
        # Skip if this is our own published message (avoid feedback loop)
        if self.last_published_stamp is not None:
            if msg.header.stamp.sec == self.last_published_stamp.sec and \
               msg.header.stamp.nanosec == self.last_published_stamp.nanosec:
                return
        
        try:
            self.rgb_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Error converting RGB image: {str(e)}')
    
    def depth_image_callback(self, msg):
        """Store depth image"""
        try:
            self.depth_image = self.cv_bridge.imgmsg_to_cv2(msg, msg.encoding)
        except Exception as e:
            self.get_logger().error(f'Error converting depth image: {str(e)}')
    
    def pixel_to_3d(self, pixel_x, pixel_y, depth_value):
        """Convert pixel coordinates to 3D point in camera frame"""
        if self.intrinsics is None:
            return None
        
        # Depth is in mm, convert to meters
        depth_m = depth_value * 0.001
        
        # Use pyrealsense2 to deproject
        point_3d = rs.rs2_deproject_pixel_to_point(
            self.intrinsics,
            [pixel_x, pixel_y],
            depth_m
        )
        
        return point_3d
    
    def detect_board_plane(self, depth_image):
        """Detect board plane using edge detection on depth image"""
        if depth_image is None:
            return None
        
        # Convert depth to meters for processing
        depth_m = depth_image.astype(np.float32) * 0.001
        
        # Find table surface (lowest points in depth)
        # Assume table is the dominant plane at the bottom
        table_depth = np.percentile(depth_m[depth_m > 0], 10)  # 10th percentile as table
        
        # Target board depth is table_depth + offset
        target_depth = table_depth + self.board_height_offset
        
        # Create mask for board plane (within threshold)
        board_mask = np.abs(depth_m - target_depth) < self.depth_threshold
        board_mask = board_mask.astype(np.uint8) * 255
        
        # Apply morphological operations to clean up
        kernel = np.ones((5, 5), np.uint8)
        board_mask = cv2.morphologyEx(board_mask, cv2.MORPH_CLOSE, kernel)
        board_mask = cv2.morphologyEx(board_mask, cv2.MORPH_OPEN, kernel)
        
        # Edge detection on depth image
        # Normalize depth for edge detection
        depth_normalized = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(depth_normalized, (5, 5), 0)
        
        # Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Combine with board mask
        combined = cv2.bitwise_and(edges, board_mask)
        
        # Dilate edges to connect nearby edges
        kernel = np.ones((3, 3), np.uint8)
        combined = cv2.dilate(combined, kernel, iterations=2)
        
        return combined, board_mask
    
    def find_board_corners(self, edge_image, board_mask):
        """Find board corners from edge detection"""
        if edge_image is None:
            return None
        
        # Find contours
        contours, _ = cv2.findContours(edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find largest contour (should be the board)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Check if contour area is reasonable
        area = cv2.contourArea(largest_contour)
        if area < 1000:  # Minimum pixel area
            return None
        
        # Approximate contour to polygon
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        
        # We need 4 corners for a rectangle
        if len(approx) < 4:
            # Try to find 4 corners using bounding box
            rect = cv2.minAreaRect(largest_contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            corners = box
        else:
            # Use the 4 corners from approximation
            corners = approx.reshape(-1, 2)
            
            # If we have more than 4, take the 4 most extreme points
            if len(corners) > 4:
                # Find extreme points
                corners = self.find_extreme_points(corners)
        
        # Sort corners: top-left, top-right, bottom-left, bottom-right
        corners_sorted = self.sort_corners(corners)
        
        return corners_sorted
    
    def find_extreme_points(self, points):
        """Find 4 extreme points from a set of points"""
        if len(points) <= 4:
            return points
        
        # Find points with min/max x+y and min/max x-y
        sums = points[:, 0] + points[:, 1]
        diffs = points[:, 0] - points[:, 1]
        
        top_left_idx = np.argmin(sums)
        bottom_right_idx = np.argmax(sums)
        top_right_idx = np.argmax(diffs)
        bottom_left_idx = np.argmin(diffs)
        
        return np.array([
            points[top_left_idx],
            points[top_right_idx],
            points[bottom_right_idx],
            points[bottom_left_idx]
        ])
    
    def sort_corners(self, corners):
        """Sort corners in order: top-left, top-right, bottom-right, bottom-left"""
        # Calculate center
        center = np.mean(corners, axis=0)
        
        # Sort by angle from center
        angles = []
        for corner in corners:
            dx = corner[0] - center[0]
            dy = corner[1] - center[1]
            angle = np.arctan2(dy, dx)
            angles.append(angle)
        
        # Sort by angle
        sorted_indices = np.argsort(angles)
        sorted_corners = corners[sorted_indices]
        
        # Find top-left (smallest x+y)
        sums = [c[0] + c[1] for c in sorted_corners]
        top_left_idx = np.argmin(sums)
        
        # Rotate to start from top-left
        sorted_corners = np.roll(sorted_corners, -top_left_idx, axis=0)
        
        return sorted_corners
    
    def transform_point_to_base_link(self, point_3d_camera):
        """Transform 3D point from camera frame to base_link frame"""
        if point_3d_camera is None:
            return None
        
        try:
            # Create PointStamped message
            point_stamped = PointStamped()
            point_stamped.header.frame_id = 'camera_color_optical_frame'
            point_stamped.header.stamp = self.get_clock().now().to_msg()
            point_stamped.point.x = point_3d_camera[0]
            point_stamped.point.y = point_3d_camera[1]
            point_stamped.point.z = point_3d_camera[2]
            
            # Transform to base_link
            transform = self.tf_buffer.lookup_transform(
                'base_link',
                'camera_color_optical_frame',
                rclpy.time.Time()
            )
            
            point_transformed = tf2_geometry_msgs.do_transform_point(point_stamped, transform)
            
            return [point_transformed.point.x, point_transformed.point.y]
        
        except Exception as e:
            self.get_logger().error(f'TF transform error: {str(e)}')
            return None
    
    def process_board_detection(self):
        """Main processing loop to detect board and publish results"""
        if self.depth_image is None or self.rgb_image is None or self.intrinsics is None:
            return
        
        # Detect board plane using edge detection
        edge_image, board_mask = self.detect_board_plane(self.depth_image)
        
        if edge_image is None:
            return
        
        # Find board corners
        corners_pixel = self.find_board_corners(edge_image, board_mask)
        
        if corners_pixel is None or len(corners_pixel) < 4:
            self.board_detected = False
            return
        
        # Convert corners to 3D points in camera frame
        corners_3d_camera = []
        for corner in corners_pixel:
            x, y = int(corner[0]), int(corner[1])
            
            # Get depth at corner
            if 0 <= y < self.depth_image.shape[0] and 0 <= x < self.depth_image.shape[1]:
                depth_value = self.depth_image[y, x]
                if depth_value > 0:
                    point_3d = self.pixel_to_3d(x, y, depth_value)
                    if point_3d:
                        corners_3d_camera.append(point_3d)
        
        if len(corners_3d_camera) < 4:
            return
        
        # Transform corners to base_link frame
        corners_base_link = []
        for point_3d in corners_3d_camera:
            corner_base = self.transform_point_to_base_link(point_3d)
            if corner_base:
                corners_base_link.append(corner_base)
        
        if len(corners_base_link) < 4:
            return
        
        # Map corners to chess board notation
        # Assuming corners are: top-left, top-right, bottom-right, bottom-left
        # Chess board: A1 (bottom-left), H1 (bottom-right), A8 (top-left), H8 (top-right)
        # But we need to determine which corner is which based on position
        # For now, assume: corners_base_link[0]=A8, corners_base_link[1]=H8, 
        #                   corners_base_link[2]=H1, corners_base_link[3]=A1
        
        # Sort by y coordinate (assuming base_link z is up, y might be forward/backward)
        # Actually, we need to understand the coordinate system better
        # Let's use the pixel positions to determine which is which
        
        # In pixel space: top-left, top-right, bottom-right, bottom-left
        # In chess: A8 (top-left), H8 (top-right), H1 (bottom-right), A1 (bottom-left)
        board_corners = {
            'A8': corners_base_link[0],  # top-left
            'H8': corners_base_link[1],  # top-right
            'H1': corners_base_link[2],  # bottom-right
            'A1': corners_base_link[3]   # bottom-left
        }
        
        # Publish corner coordinates
        corners_msg = String()
        corners_msg.data = json.dumps({
            'A1': board_corners['A1'],
            'H1': board_corners['H1'],
            'A8': board_corners['A8'],
            'H8': board_corners['H8']
        })
        self.corners_pub.publish(corners_msg)
        
        # Crop RGB image to board region
        if self.rgb_image is not None:
            # Get bounding box from corners
            x_coords = [int(c[0]) for c in corners_pixel]
            y_coords = [int(c[1]) for c in corners_pixel]
            
            x_min = max(0, min(x_coords) - 10)
            x_max = min(self.rgb_image.shape[1], max(x_coords) + 10)
            y_min = max(0, min(y_coords) - 10)
            y_max = min(self.rgb_image.shape[0], max(y_coords) + 10)
            
            # Crop image
            cropped_image = self.rgb_image[y_min:y_max, x_min:x_max]
            
            # Publish cropped image
            try:
                cropped_msg = self.cv_bridge.cv2_to_imgmsg(cropped_image, encoding='bgr8')
                cropped_msg.header.stamp = self.get_clock().now().to_msg()
                cropped_msg.header.frame_id = 'camera_color_optical_frame'
                self.last_published_stamp = cropped_msg.header.stamp
                self.cropped_image_pub.publish(cropped_msg)
            except Exception as e:
                self.get_logger().error(f'Error publishing cropped image: {str(e)}')
        
        self.board_detected = True


def main(args=None):
    rclpy.init(args=args)
    node = BoardLocatorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

