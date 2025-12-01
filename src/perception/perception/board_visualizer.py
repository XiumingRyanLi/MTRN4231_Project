#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
import json
import tf2_ros
from geometry_msgs.msg import TransformStamped
import tf_transformations


class BoardVisualizerNode(Node):
    def __init__(self):
        super().__init__('board_visualizer_node')
        
        # TF broadcaster
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        
        # Current board corners
        self.board_corners_base = None
        
        # Subscribers
        self.corners_sub = self.create_subscription(
            String,
            '/chess/board_corners_base_frame',
            self.corners_callback,
            10
        )
        
        # Publishers
        self.marker_pub = self.create_publisher(
            MarkerArray,
            '/chess/board_visualization',
            10
        )
        
        # Visualization timer
        self.viz_timer = self.create_timer(0.1, self.publish_visualization)
        
        self.get_logger().info('Board Visualizer Node initialized')
    
    def corners_callback(self, msg):
        """Store board corners in base frame"""
        try:
            self.board_corners_base = json.loads(msg.data)
            self.get_logger().debug(f'Received board corners in base frame')
        except Exception as e:
            self.get_logger().error(f'Error parsing corners: {str(e)}')
    
    def publish_visualization(self):
        """Publish RViz markers and TF frames for board corners"""
        if self.board_corners_base is None:
            return
        
        try:
            # Create marker array
            marker_array = MarkerArray()
            
            # Define corner properties
            corner_colors = {
                'A1': (1.0, 0.0, 0.0),  # Red
                'H1': (0.0, 1.0, 0.0),  # Green
                'A8': (0.0, 0.0, 1.0),  # Blue
                'H8': (1.0, 1.0, 0.0)   # Yellow
            }
            
            corner_names = ['A1', 'H1', 'A8', 'H8']
            
            for i, corner_name in enumerate(corner_names):
                if corner_name not in self.board_corners_base:
                    continue
                
                corner_data = self.board_corners_base[corner_name]
                
                # Extract coordinates
                x = corner_data['x']
                y = corner_data['y']
                z = 0.0  # Assume board is at base height
                
                # Publish TF frame for this corner
                self.publish_tf_frame(corner_name, x, y, z)
                
                # Create sphere marker for corner
                marker = Marker()
                marker.header.frame_id = 'base'
                marker.header.stamp = self.get_clock().now().to_msg()
                marker.ns = 'board_corners'
                marker.id = i
                marker.type = Marker.SPHERE
                marker.action = Marker.ADD
                
                marker.pose.position.x = x
                marker.pose.position.y = y
                marker.pose.position.z = z
                marker.pose.orientation.w = 1.0
                
                marker.scale.x = 0.03  # 3cm diameter
                marker.scale.y = 0.03
                marker.scale.z = 0.03
                
                color = corner_colors[corner_name]
                marker.color.r = color[0]
                marker.color.g = color[1]
                marker.color.b = color[2]
                marker.color.a = 1.0
                
                marker.lifetime.sec = 1
                marker_array.markers.append(marker)
                
                # Create text label
                text_marker = Marker()
                text_marker.header.frame_id = 'base'
                text_marker.header.stamp = self.get_clock().now().to_msg()
                text_marker.ns = 'board_labels'
                text_marker.id = i + 100
                text_marker.type = Marker.TEXT_VIEW_FACING
                text_marker.action = Marker.ADD
                
                text_marker.pose.position.x = x
                text_marker.pose.position.y = y
                text_marker.pose.position.z = z + 0.05  # 5cm above corner
                text_marker.pose.orientation.w = 1.0
                
                text_marker.scale.z = 0.03  # Text height
                
                text_marker.color.r = 1.0
                text_marker.color.g = 1.0
                text_marker.color.b = 1.0
                text_marker.color.a = 1.0
                
                text_marker.text = corner_name
                text_marker.lifetime.sec = 1
                marker_array.markers.append(text_marker)
            
            # Add lines connecting corners to visualize board outline
            if len(corner_names) == 4:
                line_marker = Marker()
                line_marker.header.frame_id = 'base'
                line_marker.header.stamp = self.get_clock().now().to_msg()
                line_marker.ns = 'board_outline'
                line_marker.id = 200
                line_marker.type = Marker.LINE_STRIP
                line_marker.action = Marker.ADD
                
                line_marker.scale.x = 0.01  # Line width
                
                line_marker.color.r = 1.0
                line_marker.color.g = 1.0
                line_marker.color.b = 1.0
                line_marker.color.a = 0.8
                
                # Add points in order to form rectangle: A1 -> H1 -> H8 -> A8 -> A1
                order = ['A1', 'H1', 'H8', 'A8', 'A1']
                for corner_name in order:
                    if corner_name in self.board_corners_base:
                        corner = self.board_corners_base[corner_name]
                        p = Point()
                        p.x = corner['x']
                        p.y = corner['y']
                        p.z = 0.0
                        line_marker.points.append(p)
                
                line_marker.lifetime.sec = 1
                marker_array.markers.append(line_marker)
            
            # Publish marker array
            self.marker_pub.publish(marker_array)
            
        except Exception as e:
            self.get_logger().error(f'Visualization error: {str(e)}')
    
    def publish_tf_frame(self, frame_name, x, y, z):
        """Publish TF frame for a board corner"""
        try:
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'base'
            t.child_frame_id = f'board_corner_{frame_name}'
            
            t.transform.translation.x = x
            t.transform.translation.y = y
            t.transform.translation.z = z
            
            # Identity rotation
            q = tf_transformations.quaternion_from_euler(0, 0, 0)
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]
            
            self.tf_broadcaster.sendTransform(t)
            
        except Exception as e:
            self.get_logger().error(f'TF publishing error: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    node = BoardVisualizerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()