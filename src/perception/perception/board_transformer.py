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
        self.get_logger().info(f'Sampling radius: {self.sampling_radius}')
    
    def camera_info_callback(self, msg):
        """Store camera intrinsics"""
        if self.intrinsics is not None:
            return
            
        try:
            self.get_logger().info('Receiving camera info...')
            self.intrinsics = rs.intrinsics()
            self.intrinsics.width = msg.width
            self.intrinsics.height = msg.height
            self.intrinsics.ppx = msg.k[2]
            self.intrinsics.ppy = msg.k[5]
            self.intrinsics.fx = msg.k[0]
            self.intrinsics.fy = msg.k[4]
            self.intrinsics.model = rs.distortion.brown_conrady
            self.intrinsics.coeffs = list(msg.d)
            
            self.get_logger().info(
                f'Camera intrinsics received:\n'
                f'  Resolution: {msg.width}x{msg.height}\n'
                f'  Focal length: fx={self.intrinsics.fx:.2f}, fy={self.intrinsics.fy:.2f}\n'
                f'  Principal point: ppx={self.intrinsics.ppx:.2f}, ppy={self.intrinsics.ppy:.2f}'
            )
        except Exception as e:
            self.get_logger().error(f'Error storing camera intrinsics: {str(e)}')
    
    def corners_callback(self, msg):
        """Store pixel coordinates of board corners"""
        try:
            corners_data = json.loads(msg.data)
            self.board_corners_pixel = corners_data
            self.get_logger().debug(f'Received board corners: {corners_data}')
            self.get_logger().info(
                f'Board corners updated (pixel space):\n'
                f'  A1: {corners_data.get("A1", "missing")}\n'
                f'  H1: {corners_data.get("H1", "missing")}\n'
                f'  A8: {corners_data.get("A8", "missing")}\n'
                f'  H8: {corners_data.get("H8", "missing")}',
                throttle_duration_sec=2.0
            )
        except Exception as e:
            self.get_logger().error(f'Error parsing corners: {str(e)}')
    
    def depth_callback(self, msg):
        """Store depth image"""
        try:
            self.current_depth = self.bridge.imgmsg_to_cv2(msg, 'passthrough')
            self.get_logger().debug(
                f'Depth image received: {self.current_depth.shape}, '
                f'dtype={self.current_depth.dtype}, '
                f'range=[{np.nanmin(self.current_depth):.1f}, {np.nanmax(self.current_depth):.1f}]',
                throttle_duration_sec=5.0
            )
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
            self.get_logger().warn('No depth image available')
            return float('nan')
        
        # Check bounds
        if (x_center < 0 or x_center >= self.current_depth.shape[1] or
            y_center < 0 or y_center >= self.current_depth.shape[0]):
            self.get_logger().warn(
                f'Pixel ({x_center}, {y_center}) out of bounds '
                f'({self.current_depth.shape[1]}x{self.current_depth.shape[0]})'
            )
            return float('nan')
        
        # Extract patch around center
        y_min = max(0, y_center - self.sampling_radius)
        y_max = min(self.current_depth.shape[0], y_center + self.sampling_radius + 1)
        x_min = max(0, x_center - self.sampling_radius)
        x_max = min(self.current_depth.shape[1], x_center + self.sampling_radius + 1)
        
        depth_patch = self.current_depth[y_min:y_max, x_min:x_max]
        
        # Get valid depths
        valid_depths = depth_patch[(depth_patch > 0) & ~np.isnan(depth_patch)]
        
        self.get_logger().debug(
            f'Depth sampling at ({x_center}, {y_center}): '
            f'patch size {depth_patch.shape}, {len(valid_depths)} valid pixels'
        )
        
        if len(valid_depths) < 3:
            self.get_logger().warn(
                f'Insufficient valid depth pixels at ({x_center}, {y_center}): '
                f'only {len(valid_depths)} valid points'
            )
            return float('nan')
        
        # Return median depth in meters
        depth_m = float(np.median(valid_depths)) * 0.001
        self.get_logger().debug(
            f'Depth at ({x_center}, {y_center}): {depth_m:.3f}m '
            f'(raw median: {np.median(valid_depths):.1f}mm)'
        )
        return depth_m
    
    def pixel_to_3d(self, pixel_x, pixel_y, depth_m):
        """
        Convert pixel coordinates + depth to 3D point in camera frame.
        
        Args:
            pixel_x, pixel_y (int): Pixel coordinates
            depth_m (float): Depth in meters
            
        Returns:
            list: [x, y, z] in camera frame, or None if invalid
        """
        if self.intrinsics is None:
            self.get_logger().warn('Camera intrinsics not available')
            return None
            
        if np.isnan(depth_m):
            self.get_logger().warn(f'Invalid depth (NaN) for pixel ({pixel_x}, {pixel_y})')
            return None
        
        try:
            # Deproject pixel to 3D point
            point_3d = rs.rs2_deproject_pixel_to_point(
                self.intrinsics,
                [pixel_x, pixel_y],
                depth_m
            )
            self.get_logger().debug(
                f'Deprojected ({pixel_x}, {pixel_y}, {depth_m:.3f}m) -> '
                f'camera_link: [{point_3d[0]:.3f}, {point_3d[1]:.3f}, {point_3d[2]:.3f}]'
            )
            return point_3d
        except Exception as e:
            self.get_logger().error(
                f'Deprojection error for pixel ({pixel_x}, {pixel_y}): {str(e)}'
            )
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
            
            self.get_logger().debug(
                f'Looking up transform: camera_link -> base'
            )
            
            # Look up transform
            transform = self.tf_buffer.lookup_transform(
                'base',  # Target frame
                'camera_link',  # Source frame
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=1.0)
            )
            
            self.get_logger().debug(
                f'Transform found: translation=({transform.transform.translation.x:.3f}, '
                f'{transform.transform.translation.y:.3f}, {transform.transform.translation.z:.3f})'
            )
            
            # Transform point
            point_transformed = tf2_geometry_msgs.do_transform_point(point_stamped, transform)
            
            result = [
                point_transformed.point.x,
                point_transformed.point.y
            ]
            
            self.get_logger().debug(
                f'Transformed camera_link [{point_camera[0]:.3f}, {point_camera[1]:.3f}, {point_camera[2]:.3f}] -> '
                f'base [{result[0]:.3f}, {result[1]:.3f}]'
            )
            
            return result
            
        except tf2_ros.LookupException as e:
            self.get_logger().error(f'TF lookup failed (frames may not exist): {str(e)}')
            return None
        except tf2_ros.ConnectivityException as e:
            self.get_logger().error(f'TF connectivity error: {str(e)}')
            return None
        except tf2_ros.ExtrapolationException as e:
            self.get_logger().error(f'TF extrapolation error (timing issue): {str(e)}')
            return None
        except Exception as e:
            self.get_logger().error(f'Unexpected TF error: {str(e)}')
            return None
    
    def process_transformation(self):
        """
        Main processing loop: transform board corners from pixel space to base frame.
        """
        # Log status of all prerequisites
        self.get_logger().debug(
            f'Transformation check: '
            f'corners={self.board_corners_pixel is not None}, '
            f'depth={self.current_depth is not None}, '
            f'intrinsics={self.intrinsics is not None}',
            throttle_duration_sec=5.0
        )
        
        # Check prerequisites
        if self.board_corners_pixel is None:
            self.get_logger().warn('Waiting for board corners...', throttle_duration_sec=5.0)
            return
        
        if self.current_depth is None:
            self.get_logger().warn('Waiting for depth image...', throttle_duration_sec=5.0)
            return
        
        if self.intrinsics is None:
            self.get_logger().warn('Waiting for camera intrinsics...', throttle_duration_sec=5.0)
            return
        
        self.get_logger().info('✓ All prerequisites met, processing transformation...', throttle_duration_sec=2.0)
        
        # Process each corner
        corners_base = {}
        
        for corner_name in ['A1', 'H1', 'A8', 'H8']:
            if corner_name not in self.board_corners_pixel:
                self.get_logger().warn(f'Missing corner: {corner_name}')
                return
            
            self.get_logger().debug(f'Processing corner: {corner_name}')
            
            # Get pixel coordinates (assuming they're [x, y] from board_locator)
            pixel_coords = self.board_corners_pixel[corner_name]
            
            # Handle both list and individual coordinates
            if isinstance(pixel_coords, list) and len(pixel_coords) >= 2:
                pixel_x = int(pixel_coords[0])
                pixel_y = int(pixel_coords[1])
            else:
                self.get_logger().error(
                    f'Invalid pixel format for {corner_name}: {pixel_coords} '
                    f'(type: {type(pixel_coords)})'
                )
                return
            
            self.get_logger().debug(f'{corner_name}: pixel=({pixel_x}, {pixel_y})')
            
            # Get depth at this pixel
            depth_m = self.get_average_depth(pixel_x, pixel_y)
            
            if np.isnan(depth_m):
                self.get_logger().warn(f'Invalid depth for corner {corner_name}')
                return
            
            self.get_logger().debug(f'{corner_name}: depth={depth_m:.3f}m')
            
            # Convert to 3D point in camera frame
            point_3d_camera = self.pixel_to_3d(pixel_x, pixel_y, depth_m)
            
            if point_3d_camera is None:
                self.get_logger().warn(f'Failed to deproject {corner_name}')
                return
            
            self.get_logger().debug(
                f'{corner_name}: camera_3d=[{point_3d_camera[0]:.3f}, '
                f'{point_3d_camera[1]:.3f}, {point_3d_camera[2]:.3f}]'
            )
            
            # Transform to base frame
            point_base = self.transform_to_base(point_3d_camera)
            
            if point_base is None:
                self.get_logger().warn(f'Failed to transform {corner_name} to base frame')
                return
            
            self.get_logger().debug(
                f'{corner_name}: base_2d=[{point_base[0]:.3f}, {point_base[1]:.3f}]'
            )
            
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
                f'✓ Board corners transformed to base frame:\n'
                f'  A1: [{corners_base["A1"][0]:.3f}, {corners_base["A1"][1]:.3f}]\n'
                f'  H1: [{corners_base["H1"][0]:.3f}, {corners_base["H1"][1]:.3f}]\n'
                f'  A8: [{corners_base["A8"][0]:.3f}, {corners_base["A8"][1]:.3f}]\n'
                f'  H8: [{corners_base["H8"][0]:.3f}, {corners_base["H8"][1]:.3f}]',
                throttle_duration_sec=2.0
            )
        else:
            self.get_logger().warn(
                f'Incomplete corner set: only {len(corners_base)}/4 corners processed'
            )


def main(args=None):
    rclpy.init(args=args)
    node = BoardTransformerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()