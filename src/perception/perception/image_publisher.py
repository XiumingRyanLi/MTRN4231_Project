#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
from ament_index_python.packages import get_package_share_directory

class ImagePublisherNode(Node):
    def __init__(self):
        super().__init__('image_publisher_node')
        
        # Parameters
        self.declare_parameter('image_path', 'test-images/test_cam4.jpg')
        self.declare_parameter('publish_rate', 1.0)  # Hz
        self.declare_parameter('output_topic', '/camera/image_raw')
<<<<<<< HEAD
        self.declare_parameter('loop', True)  # Keep publishing or publish once
=======
        self.declare_parameter('once', True)  # Keep publishing or publish once
>>>>>>> 62a18b07e0594dc6d78e18139c352180c7cc4e79
        self.declare_parameter('use_package_path', False)  # If true, look in package share directory
        
        # Get parameters
        image_path_param = self.get_parameter('image_path').value
        publish_rate = self.get_parameter('publish_rate').value
        output_topic = self.get_parameter('output_topic').value
<<<<<<< HEAD
        self.loop = self.get_parameter('loop').value
=======
        self.loop = self.get_parameter('once').value
>>>>>>> 62a18b07e0594dc6d78e18139c352180c7cc4e79
        use_package_path = self.get_parameter('use_package_path').value
        
        # Determine full image path
        if use_package_path:
            try:
                package_dir = get_package_share_directory('chess_board_detector')
                self.image_path = os.path.join(package_dir, image_path_param)
            except Exception:
                self.get_logger().warn('Could not find package directory, using relative path')
                self.image_path = image_path_param
        else:
            # If path is relative, try to resolve it from current directory
            if not os.path.isabs(image_path_param):
                # Try current directory first
                if os.path.exists(image_path_param):
                    self.image_path = os.path.abspath(image_path_param)
                # Try relative to home
                elif os.path.exists(os.path.expanduser(f'~/{image_path_param}')):
                    self.image_path = os.path.expanduser(f'~/{image_path_param}')
                # Try relative to workspace src
                elif os.path.exists(os.path.expanduser(f'~/MTRN4231_Project/src/perception/{image_path_param}')):
                    self.image_path = os.path.expanduser(f'~/MTRN4231_Project/src/perception/{image_path_param}')
                else:
                    self.image_path = image_path_param
            else:
                self.image_path = image_path_param
        
        # Validate image path
        if not os.path.exists(self.image_path):
            self.get_logger().error(f'Image not found: {self.image_path}')
            self.get_logger().error(f'Searched paths:')
            self.get_logger().error(f'  - {os.path.abspath(image_path_param)}')
            self.get_logger().error(f'  - {os.path.expanduser(f"~/{image_path_param}")}')
            self.get_logger().error(f'  - {os.path.expanduser(f"~/ros2_ws/src/{image_path_param}")}')
            raise FileNotFoundError(f'Image not found: {self.image_path}')
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Load image
        self.cv_image = cv2.imread(self.image_path)
        if self.cv_image is None:
            self.get_logger().error(f'Failed to load image: {self.image_path}')
            raise ValueError(f'Could not read image: {self.image_path}')
        
        self.get_logger().info(f'Successfully loaded image: {self.image_path}')
        self.get_logger().info(f'Image shape: {self.cv_image.shape}')
        
        # Publisher
        self.image_pub = self.create_publisher(Image, output_topic, 10)
        
        # Timer for publishing
        timer_period = 1.0 / publish_rate
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.publish_count = 0
        self.get_logger().info(f'Publishing to: {output_topic} at {publish_rate} Hz')
        
    def timer_callback(self):
        """Publish the image"""
        try:
            # Convert OpenCV image to ROS Image message
            ros_image = self.bridge.cv2_to_imgmsg(self.cv_image, encoding='bgr8')
            
            # Set timestamp
            ros_image.header.stamp = self.get_clock().now().to_msg()
            ros_image.header.frame_id = 'camera'
            
            # Publish
            self.image_pub.publish(ros_image)
            
            self.publish_count += 1
            if self.publish_count == 1 or self.publish_count % 10 == 0:
                self.get_logger().info(f'Published image #{self.publish_count}')
            
            # Stop after one publish if loop is false
            if not self.loop and self.publish_count >= 1:
                self.get_logger().info('Published once. Shutting down...')
                self.timer.cancel()
                
        except Exception as e:
            self.get_logger().error(f'Error publishing image: {str(e)}')


class ImageDirectoryPublisherNode(Node):
    """Publisher for cycling through multiple images in a directory"""
    def __init__(self):
        super().__init__('image_directory_publisher_node')
        
        # Parameters
        self.declare_parameter('image_directory', 'test-images')
        self.declare_parameter('publish_rate', 1.0)  # Hz
        self.declare_parameter('output_topic', '/camera/image_raw')
        self.declare_parameter('loop', True)
        
        # Get parameters
        image_dir_param = self.get_parameter('image_directory').value
        publish_rate = self.get_parameter('publish_rate').value
        output_topic = self.get_parameter('output_topic').value
        self.loop = self.get_parameter('loop').value
        
        # Resolve directory path
        if not os.path.isabs(image_dir_param):
            if os.path.exists(image_dir_param):
                self.image_dir = os.path.abspath(image_dir_param)
            elif os.path.exists(os.path.expanduser(f'~/{image_dir_param}')):
                self.image_dir = os.path.expanduser(f'~/{image_dir_param}')
            elif os.path.exists(os.path.expanduser(f'~/ros2_ws/src/{image_dir_param}')):
                self.image_dir = os.path.expanduser(f'~/ros2_ws/src/{image_dir_param}')
            else:
                self.image_dir = image_dir_param
        else:
            self.image_dir = image_dir_param
        
        # Validate directory
        if not os.path.exists(self.image_dir):
            self.get_logger().error(f'Directory not found: {self.image_dir}')
            raise FileNotFoundError(f'Directory not found: {self.image_dir}')
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        self.image_files = []
        for file in sorted(os.listdir(self.image_dir)):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                self.image_files.append(os.path.join(self.image_dir, file))
        
        if not self.image_files:
            self.get_logger().error(f'No images found in: {self.image_dir}')
            raise ValueError(f'No images in directory: {self.image_dir}')
        
        self.get_logger().info(f'Found {len(self.image_files)} images in {self.image_dir}')
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Publisher
        self.image_pub = self.create_publisher(Image, output_topic, 10)
        
        # Timer for publishing
        timer_period = 1.0 / publish_rate
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.current_index = 0
        self.get_logger().info(f'Publishing to: {output_topic} at {publish_rate} Hz')
        
    def timer_callback(self):
        """Publish the next image in sequence"""
        try:
            # Load current image
            image_path = self.image_files[self.current_index]
            cv_image = cv2.imread(image_path)
            
            if cv_image is None:
                self.get_logger().error(f'Failed to load: {image_path}')
                self.current_index = (self.current_index + 1) % len(self.image_files)
                return
            
            # Convert to ROS message
            ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
            ros_image.header.stamp = self.get_clock().now().to_msg()
            ros_image.header.frame_id = 'camera'
            
            # Publish
            self.image_pub.publish(ros_image)
            
            self.get_logger().info(f'Published: {os.path.basename(image_path)} '
                                  f'({self.current_index + 1}/{len(self.image_files)})')
            
            # Move to next image
            self.current_index += 1
            
            # Handle looping
            if self.current_index >= len(self.image_files):
                if self.loop:
                    self.current_index = 0
                    self.get_logger().info('Looping back to first image')
                else:
                    self.get_logger().info('All images published. Shutting down...')
                    self.timer.cancel()
                    
        except Exception as e:
            self.get_logger().error(f'Error publishing image: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    
    # Check if directory mode is requested
    import sys
    if '--directory' in sys.argv or '-d' in sys.argv:
        node = ImageDirectoryPublisherNode()
    else:
        node = ImagePublisherNode()
    
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