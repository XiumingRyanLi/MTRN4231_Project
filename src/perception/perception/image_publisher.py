#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__('camera_publisher_node')
        
        # Parameters
        self.declare_parameter('camera_index', 0)  # 0 for default camera, 1, 2, etc. for others
        self.declare_parameter('publish_rate', 30.0)  # Hz
        self.declare_parameter('output_topic', '/camera/image_raw')
        self.declare_parameter('frame_width', 640)
        self.declare_parameter('frame_height', 480)
        
        # Get parameters
        camera_index = self.get_parameter('camera_index').value
        publish_rate = self.get_parameter('publish_rate').value
        output_topic = self.get_parameter('output_topic').value
        frame_width = self.get_parameter('frame_width').value
        frame_height = self.get_parameter('frame_height').value
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Open camera
        self.get_logger().info(f'Opening camera {camera_index}...')
        self.cap = cv2.VideoCapture(camera_index)
        
        if not self.cap.isOpened():
            self.get_logger().error(f'Failed to open camera {camera_index}')
            raise RuntimeError(f'Could not open camera {camera_index}')
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        
        # Get actual camera properties (may differ from requested)
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        self.get_logger().info(f'Camera opened successfully')
        self.get_logger().info(f'Resolution: {actual_width}x{actual_height}')
        self.get_logger().info(f'Camera FPS: {actual_fps}')
        
        # Publisher
        self.image_pub = self.create_publisher(Image, output_topic, 10)
        
        # Timer for publishing
        timer_period = 1.0 / publish_rate
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.frame_count = 0
        self.get_logger().info(f'Publishing to: {output_topic} at {publish_rate} Hz')
        
    def timer_callback(self):
        """Capture and publish camera frame"""
        try:
            # Capture frame
            ret, frame = self.cap.read()
            
            if not ret or frame is None:
                self.get_logger().warn('Failed to capture frame')
                return
            
            # Convert OpenCV image to ROS Image message
            ros_image = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            
            # Set timestamp
            ros_image.header.stamp = self.get_clock().now().to_msg()
            ros_image.header.frame_id = 'camera'
            
            # Publish
            self.image_pub.publish(ros_image)
            
            self.frame_count += 1
            if self.frame_count == 1 or self.frame_count % 100 == 0:
                self.get_logger().info(f'Published frame #{self.frame_count}')
                
        except Exception as e:
            self.get_logger().error(f'Error capturing/publishing frame: {str(e)}')
    
    def destroy_node(self):
        """Clean up resources"""
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
            self.get_logger().info('Camera released')
        super().destroy_node()


class SnapshotPublisherNode(Node):
    """Captures a single snapshot from camera and publishes it repeatedly"""
    def __init__(self):
        super().__init__('snapshot_publisher_node')
        
        # Parameters
        self.declare_parameter('camera_index', 0)
        self.declare_parameter('publish_rate', 1.0)  # Hz
        self.declare_parameter('output_topic', '/camera/image_raw')
        self.declare_parameter('frame_width', 640)
        self.declare_parameter('frame_height', 480)
        self.declare_parameter('loop', False)  # Keep publishing or publish once
        
        # Get parameters
        camera_index = self.get_parameter('camera_index').value
        publish_rate = self.get_parameter('publish_rate').value
        output_topic = self.get_parameter('output_topic').value
        frame_width = self.get_parameter('frame_width').value
        frame_height = self.get_parameter('frame_height').value
        self.loop = self.get_parameter('loop').value
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Open camera temporarily to capture snapshot
        self.get_logger().info(f'Opening camera {camera_index} for snapshot...')
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            self.get_logger().error(f'Failed to open camera {camera_index}')
            raise RuntimeError(f'Could not open camera {camera_index}')
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        
        # Warm up camera (capture a few frames)
        self.get_logger().info('Warming up camera...')
        for _ in range(5):
            cap.read()
        
        # Capture snapshot
        ret, self.snapshot = cap.read()
        cap.release()
        
        if not ret or self.snapshot is None:
            self.get_logger().error('Failed to capture snapshot')
            raise RuntimeError('Could not capture snapshot from camera')
        
        self.get_logger().info(f'Snapshot captured: {self.snapshot.shape}')
        
        # Publisher
        self.image_pub = self.create_publisher(Image, output_topic, 10)
        
        # Timer for publishing
        timer_period = 1.0 / publish_rate
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.publish_count = 0
        self.get_logger().info(f'Publishing snapshot to: {output_topic} at {publish_rate} Hz')
        
    def timer_callback(self):
        """Publish the snapshot"""
        try:
            # Convert OpenCV image to ROS Image message
            ros_image = self.bridge.cv2_to_imgmsg(self.snapshot, encoding='bgr8')
            
            # Set timestamp
            ros_image.header.stamp = self.get_clock().now().to_msg()
            ros_image.header.frame_id = 'camera'
            
            # Publish
            self.image_pub.publish(ros_image)
            
            self.publish_count += 1
            if self.publish_count == 1 or self.publish_count % 10 == 0:
                self.get_logger().info(f'Published snapshot #{self.publish_count}')
            
            # Stop after one publish if loop is false
            if not self.loop and self.publish_count >= 1:
                self.get_logger().info('Published once. Shutting down...')
                self.timer.cancel()
                
        except Exception as e:
            self.get_logger().error(f'Error publishing snapshot: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    
    # Check which mode is requested
    import sys
    if '--snapshot' in sys.argv or '-s' in sys.argv:
        node = SnapshotPublisherNode()
    else:
        node = CameraPublisherNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()