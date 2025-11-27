#!/usr/bin/env python3

import rclpy
import tf2_ros
from geometry_msgs.msg import Point, Pose, TransformStamped, Quaternion
import tf_transformations
from rclpy.time import Time
import pyrealsense2 as rs
from sensor_msgs.msg import CameraInfo
import tf2_geometry_msgs


class TFHandler:
    """
    Handles all TF transformations and camera intrinsics for the chess detection system.
    
    This class provides utilities for:
    - Camera intrinsics management
    - Pixel-to-3D point conversion
    - Frame transformations (camera <-> base)
    - TF broadcasting
    """
    
    def __init__(self, node):
        """
        Initialize TF handler.
        
        Args:
            node: ROS2 node instance
        """
        self.node = node
        
        # TF buffer and listener for receiving transforms
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self.node)
        
        # TF broadcaster for publishing transforms
        self.broadcaster = tf2_ros.TransformBroadcaster(self.node)
        
        # Camera intrinsics (populated from CameraInfo)
        self.intrinsics = None
        
        # Subscribe to camera info to get intrinsics
        self.cam_info_sub = self.node.create_subscription(
            CameraInfo,
            '/camera/camera/aligned_depth_to_color/camera_info',
            self.camera_info_callback,
            10
        )
        
        self.node.get_logger().info('TF Handler initialized')
    
    def camera_info_callback(self, msg):
        """
        Store camera intrinsics when available.
        
        Args:
            msg (CameraInfo): Camera information message
        """
        if self.intrinsics is None:
            try:
                self.intrinsics = rs.intrinsics()
                self.intrinsics.width = msg.width
                self.intrinsics.height = msg.height
                self.intrinsics.ppx = msg.k[2]  # Principal point x
                self.intrinsics.ppy = msg.k[5]  # Principal point y
                self.intrinsics.fx = msg.k[0]   # Focal length x
                self.intrinsics.fy = msg.k[4]   # Focal length y
                
                # Handle distortion model
                if msg.distortion_model == 'plumb_bob':
                    self.intrinsics.model = rs.distortion.brown_conrady
                elif msg.distortion_model == 'equidistant':
                    self.intrinsics.model = rs.distortion.kannala_brandt4
                else:
                    self.intrinsics.model = rs.distortion.brown_conrady
                
                self.intrinsics.coeffs = list(msg.d)
                
                self.node.get_logger().info(
                    f"Camera intrinsics received: "
                    f"{msg.width}x{msg.height}, "
                    f"fx={self.intrinsics.fx:.2f}, "
                    f"fy={self.intrinsics.fy:.2f}"
                )
            except Exception as e:
                self.node.get_logger().error(f"Error setting camera intrinsics: {str(e)}")
    
    def pixel_to_3d(self, pixel_x, pixel_y, depth_value):
        """
        Convert pixel coordinates and depth to 3D point in camera frame.
        
        Args:
            pixel_x (int/float): Pixel x coordinate
            pixel_y (int/float): Pixel y coordinate
            depth_value (float): Depth value in millimeters
            
        Returns:
            list: [x, y, z] in camera frame (meters), or None if conversion fails
        """
        if self.intrinsics is None:
            self.node.get_logger().warn("Camera intrinsics not available")
            return None
        
        try:
            # Convert depth from mm to meters
            depth_m = depth_value * 0.001
            
            # Deproject pixel to 3D point using RealSense intrinsics
            point_3d = rs.rs2_deproject_pixel_to_point(
                self.intrinsics,
                [float(pixel_x), float(pixel_y)],
                depth_m
            )
            
            return point_3d
            
        except Exception as e:
            self.node.get_logger().error(f"Pixel to 3D conversion error: {str(e)}")
            return None
    
    def transform_to_base(self, point, from_frame='camera_link'):
        """
        Transform a point from a given frame to the robot base frame.
        
        Args:
            point (Point): Point in source frame
            from_frame (str): Source frame name (default: 'camera_link')
            
        Returns:
            Point: Transformed point in base frame, or None if transform fails
        """
        try:
            # Check if transform is available
            if not self.tf_buffer.can_transform(
                'base', 
                from_frame, 
                rclpy.time.Time(), 
                rclpy.duration.Duration(seconds=2.0)
            ):
                self.node.get_logger().error(
                    f'TF transform not available from {from_frame} to base'
                )
                return None
            
            # Lookup transform
            transform = self.tf_buffer.lookup_transform(
                'base',  # Target frame
                from_frame,  # Source frame
                rclpy.time.Time(),  # Latest available
                timeout=rclpy.duration.Duration(seconds=2.0)
            )
            
            # Create Pose with the point
            pose = Pose()
            pose.position = point
            pose.orientation = Quaternion()  # Identity quaternion
            pose.orientation.w = 1.0
            
            # Transform the pose
            transformed_pose = tf2_geometry_msgs.do_transform_pose(pose, transform)
            
            return transformed_pose.position
            
        except (tf2_ros.LookupException, 
                tf2_ros.ConnectivityException, 
                tf2_ros.ExtrapolationException) as e:
            self.node.get_logger().error(f"TF transform error: {str(e)}")
            return None
    
    def transform_point_stamped(self, point_stamped, target_frame='base'):
        """
        Transform a PointStamped message to target frame.
        
        Args:
            point_stamped (PointStamped): Point with frame information
            target_frame (str): Target frame name
            
        Returns:
            PointStamped: Transformed point, or None if transform fails
        """
        try:
            # Lookup transform
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                point_stamped.header.frame_id,
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=2.0)
            )
            
            # Transform point
            transformed_point = tf2_geometry_msgs.do_transform_point(
                point_stamped, 
                transform
            )
            
            return transformed_point
            
        except Exception as e:
            self.node.get_logger().error(f"Point transform error: {str(e)}")
            return None
    
    def publish_transform(self, frame_id, child_frame_id, point, orientation=None):
        """
        Publish a TF transform.
        
        Args:
            frame_id (str): Parent frame name
            child_frame_id (str): Child frame name
            point (list/tuple): Translation [x, y, z]
            orientation (Quaternion, optional): Rotation quaternion
        """
        try:
            t = TransformStamped()
            t.header.stamp = self.node.get_clock().now().to_msg()
            t.header.frame_id = frame_id
            t.child_frame_id = child_frame_id
            
            # Set translation
            t.transform.translation.x = float(point[0])
            t.transform.translation.y = float(point[1])
            t.transform.translation.z = float(point[2])
            
            # Set rotation
            if orientation is None:
                # Identity rotation (no rotation)
                q = tf_transformations.quaternion_from_euler(0, 0, 0)
                t.transform.rotation.x = q[0]
                t.transform.rotation.y = q[1]
                t.transform.rotation.z = q[2]
                t.transform.rotation.w = q[3]
            else:
                t.transform.rotation = orientation
            
            # Broadcast transform
            self.broadcaster.sendTransform(t)
            
        except Exception as e:
            self.node.get_logger().error(f"Transform publish error: {str(e)}")
    
    def get_transform(self, target_frame, source_frame, time=None):
        """
        Get transform between two frames.
        
        Args:
            target_frame (str): Target frame name
            source_frame (str): Source frame name
            time (Time, optional): Time at which to get transform
            
        Returns:
            TransformStamped: Transform, or None if lookup fails
        """
        try:
            if time is None:
                time = rclpy.time.Time()
            
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                source_frame,
                time,
                timeout=rclpy.duration.Duration(seconds=1.0)
            )
            
            return transform
            
        except Exception as e:
            self.node.get_logger().error(
                f"Failed to get transform from {source_frame} to {target_frame}: {str(e)}"
            )
            return None
    
    def transform_camera_to_world(self, point):
        """
        DEPRECATED: Manual coordinate transformation from camera to world frame.
        This is a custom transformation that may be specific to your robot setup.
        Consider using transform_to_base() instead for general use.
        
        Args:
            point (list): [x, y, z] in camera frame
            
        Returns:
            list: [x, y, z] in world frame
        """
        # Custom transformation based on your robot's coordinate system
        # These offsets should be replaced with proper TF transformations
        return [
            point[2],                    # Camera Z -> World X (forward)
            -point[1] + 0.038 + 0.20,   # Camera -Y + offset -> World Y
            -point[0] - 0.18,           # Camera -X + offset -> World Z
        ]
    
    def wait_for_transform(self, target_frame, source_frame, timeout=5.0):
        """
        Wait for a transform to become available.
        
        Args:
            target_frame (str): Target frame name
            source_frame (str): Source frame name
            timeout (float): Timeout in seconds
            
        Returns:
            bool: True if transform is available, False otherwise
        """
        try:
            start_time = self.node.get_clock().now()
            timeout_duration = rclpy.duration.Duration(seconds=timeout)
            
            while rclpy.ok():
                if self.tf_buffer.can_transform(
                    target_frame, 
                    source_frame, 
                    rclpy.time.Time()
                ):
                    return True
                
                # Check timeout
                if (self.node.get_clock().now() - start_time) > timeout_duration:
                    self.node.get_logger().warn(
                        f"Timeout waiting for transform from {source_frame} to {target_frame}"
                    )
                    return False
                
                rclpy.spin_once(self.node, timeout_sec=0.1)
            
            return False
            
        except Exception as e:
            self.node.get_logger().error(f"Error waiting for transform: {str(e)}")
            return False