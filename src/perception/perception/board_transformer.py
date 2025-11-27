#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point, PointStamped
from sensor_msgs.msg import Image
import json
import numpy as np
from cv_bridge import CvBridge
import pyrealsense2 as rs
from sensor_msgs.msg import CameraInfo
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import Quaternion, Pose


class BoardTransformerNode(Node):
    def __init__(self):
        super().__init__('board_transformer_node')
        
        # Parameters
        self.declare_parameter('sampling_radius', 5)
        self.sampling_radius = self.get_parameter('sampling_radius').value
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Camera intrinsics
        self.intrinsics = None
        
        # Current frames
        self.current_depth = None
        self.board_corners_pixel = None
        
        # TF setup
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
        # Subscribers
        self.corners_sub = self.create_subscription(
            String,
            '/chess/board_corners',
            self.corners_callback,
            10
        )
        
        self.depth_sub = self.create_subscription(
            Image,
            '/camera/camera/aligned_depth_to_color/image_raw',
            self.depth_callback,
            10
        )
        
        self.cam_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/camera/aligned_depth_to_color/camera_info',
            self.camera_info_callback,
            10
        )
        
        # Publishers
        self.board_corners_base_pub = self.create_publisher(
            String,
            '/chess/board_corners_base_frame',
            10
        )
        
        # Processing timer
        self.timer = self.create_timer(0.1, self.process_transformation)
        
        self.get_logger().info('Board Transformer Node initialized')
    
    def camera_info_callback(self, msg):
        """Store camera intrinsics"""
        if self.intrinsics is not None:
            return
            
        try:
            self.intrinsics = rs.intrinsics()
            self.intrinsics.width = msg.width
            self.intrinsics.height = msg.height
            self.intrinsics.ppx = msg.k[2]
            self.intrinsics.ppy = msg.k[5]
            self.intrinsics.fx = msg.k[0]
            self.intrinsics.fy = msg.k[4]
            self.intrinsics.model = rs.distortion.brown_conrady
            self.intrinsics.coeffs = list(msg.d)
            
            self.get_logger().info('Camera intrinsics received')
        except Exception as e:
            self.get_logger().error(f'Error storing camera intrinsics: {str(e)}')
    
    def corners_callback(self, msg):
        """Store pixel coordinates of board corners"""
        try:
            corners_data = json.loads(msg.data)
            self.board_corners_pixel = corners_data
            self.get_logger().debug(f'Received board corners: {corners_data}')
        except Exception as e:
            self.get_logger().error(f'Error parsing corners: {str(e)}')
    
    def depth_callback(self, msg):
        """Store depth image"""
        try:
            self.current_depth = self.bridge.imgmsg_to_cv2(msg, 'passthrough')
        except Exception as e:
            self.get_logger().error(f'Error converting depth image: {str(e)}')
    
    def get_average_depth(self, x_center, y_center):
        """
        Get robust depth estimate at pixel location.
        
        Args:
            x_center, y_center (int): Pixel coordinates
            
        Returns:
            float: Median depth in meters, or NaN if invalid
        """
        if self.current_depth is None:
            return float('nan')
        
        # Extract patch around center
        depth_patch = self.current_depth[
            max(0, y_center - self.sampling_radius):min(self.current_depth.shape[0], y_center + self.sampling_radius + 1),
            max(0, x_center - self.sampling_radius):min(self.current_depth.shape[1], x_center + self.sampling_radius + 1)
        ]
        
        # Get valid depths
        valid_depths = depth_patch[(depth_patch > 0) & ~np.isnan(depth_patch)]
        
        if len(valid_depths) < 3:
            return float('nan')
        
        # Return median depth in meters
        return float(np.median(valid_depths)) * 0.001
    
    def pixel_to_3d(self, pixel_x, pixel_y, depth_m):
        """
        Convert pixel coordinates + depth to 3D point in camera frame.
        
        Args:
            pixel_x, pixel_y (int): Pixel coordinates
            depth_m (float): Depth in meters
            
        Returns:
            list: [x, y, z] in camera frame, or None if invalid
        """
        if self.intrinsics is None or np.isnan(depth_m):
            return None
        
        try:
            # Deproject pixel to 3D point
            point_3d = rs.rs2_deproject_pixel_to_point(
                self.intrinsics,
                [pixel_x, pixel_y],
                depth_m
            )
            return point_3d
        except Exception as e:
            self.get_logger().error(f'Deprojection error: {str(e)}')
            return None
    
    def transform_to_base(self, point_camera):
        """
        Transform 3D point from camera frame to robot base frame.
        
        Args:
            point_camera (list): [x, y, z] in camera_link frame
            
        Returns:
            list: [x, y] in base frame, or None if transform fails
        """
        try:
            # Create PointStamped message
            point_stamped = PointStamped()
            point_stamped.header.frame_id = 'camera_link'
            point_stamped.header.stamp = self.get_clock().now().to_msg()
            point_stamped.point.x = point_camera[0]
            point_stamped.point.y = point_camera[1]
            point_stamped.point.z = point_camera[2]
            
            # Look up transform
            transform = self.tf_buffer.lookup_transform(
                'base',  # Target frame
                'camera_link',  # Source frame
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=1.0)
            )
            
            # Transform point
            point_transformed = tf2_geometry_msgs.do_transform_point(point_stamped, transform)
            
            # Return as [x, y] in base frame
            return [
                point_transformed.point.x,
                point_transformed.point.y
            ]
            
        except (tf2_ros.LookupException, 
                tf2_ros.ConnectivityException, 
                tf2_ros.ExtrapolationException) as e:
            self.get_logger().error(f'TF transform failed: {str(e)}')
            return None
    
    def process_transformation(self):
        """
        Main processing loop: transform board corners from pixel space to base frame.
        """
        if self.board_corners_pixel is None:
            return
        
        if self.current_depth is None:
            return
        
        if self.intrinsics is None:
            return
        
        # Process each corner
        corners_base = {}
        
        for corner_name in ['A1', 'H1', 'A8', 'H8']:
            if corner_name not in self.board_corners_pixel:
                self.get_logger().warn(f'Missing corner: {corner_name}')
                return
            
            # Get pixel coordinates (assuming they're [x, y] from board_locator)
            pixel_coords = self.board_corners_pixel[corner_name]
            
            # Handle both list and individual coordinates
            if isinstance(pixel_coords, list) and len(pixel_coords) >= 2:
                pixel_x = int(pixel_coords[0])
                pixel_y = int(pixel_coords[1])
            else:
                self.get_logger().error(f'Invalid pixel format for {corner_name}')
                return
            
            # Get depth at this pixel
            depth_m = self.get_average_depth(pixel_x, pixel_y)
            
            if np.isnan(depth_m):
                self.get_logger().warn(f'Invalid depth for corner {corner_name}')
                return
            
            # Convert to 3D point in camera frame
            point_3d_camera = self.pixel_to_3d(pixel_x, pixel_y, depth_m)
            
            if point_3d_camera is None:
                self.get_logger().warn(f'Failed to deproject {corner_name}')
                return
            
            # Transform to base frame
            point_base = self.transform_to_base(point_3d_camera)
            
            if point_base is None:
                self.get_logger().warn(f'Failed to transform {corner_name}')
                return
            
            corners_base[corner_name] = point_base
        
        # Publish transformed corners
        if len(corners_base) == 4:
            corners_msg = String()
            corners_msg.data = json.dumps({
                'A1': {'x': corners_base['A1'][0], 'y': corners_base['A1'][1]},
                'H1': {'x': corners_base['H1'][0], 'y': corners_base['H1'][1]},
                'A8': {'x': corners_base['A8'][0], 'y': corners_base['A8'][1]},
                'H8': {'x': corners_base['H8'][0], 'y': corners_base['H8'][1]}
            })
            self.board_corners_base_pub.publish(corners_msg)
            
            self.get_logger().info(
                f'Board corners in base frame:\n'
                f'  A1: [{corners_base["A1"][0]:.3f}, {corners_base["A1"][1]:.3f}]\n'
                f'  H1: [{corners_base["H1"][0]:.3f}, {corners_base["H1"][1]:.3f}]\n'
                f'  A8: [{corners_base["A8"][0]:.3f}, {corners_base["A8"][1]:.3f}]\n'
                f'  H8: [{corners_base["H8"][0]:.3f}, {corners_base["H8"][1]:.3f}]',
                throttle_duration_sec=2.0
            )


def main(args=None):
    rclpy.init(args=args)
    node = BoardTransformerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()