#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from typing import Optional, Dict
from scipy.spatial.transform import Rotation

# Map easy param strings to OpenCV constants
DICT_OPTIONS: Dict[str, int] = {
    "DICT_4X4_50":  cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
}

def get_aruco_dictionary(name: str):
    # Compatible across OpenCV 4.x variants
    if not hasattr(cv2, "aruco"):
        raise RuntimeError("Your OpenCV build lacks cv2.aruco. Install opencv-contrib.")
    dconst = DICT_OPTIONS.get(name.upper(), cv2.aruco.DICT_4X4_50)
    try:
        return cv2.aruco.getPredefinedDictionary(dconst)
    except AttributeError:
        # Older OpenCV API
        return cv2.aruco.Dictionary_get(dconst)

def get_aruco_detector_params():
    try:
        return cv2.aruco.DetectorParameters_create()
    except AttributeError:
        # Newer API uses DetectorParameters in constructor of ArucoDetector
        return None

class ArucoDetectorNode(Node):
    def __init__(self):
        super().__init__("aruco_detector")

        # Parameters
        self.declare_parameter("dictionary", "DICT_4X4_50")
        self.declare_parameter("topic", "/camera/camera/color/image_raw")
        self.declare_parameter("desired_encoding", "bgr8")
        self.declare_parameter("marker_size", 0.05)  # marker size in meters
        self.declare_parameter("camera_matrix", [])  # 3x3 camera intrinsic matrix (flattened)
        self.declare_parameter("dist_coeffs", [])    # distortion coefficients

        dict_name = self.get_parameter("dictionary").get_parameter_value().string_value
        topic = self.get_parameter("topic").get_parameter_value().string_value
        self.desired_encoding = self.get_parameter("desired_encoding").get_parameter_value().string_value
        self.marker_size = self.get_parameter("marker_size").get_parameter_value().double_value
        
        # Camera calibration parameters
        camera_matrix_flat = self.get_parameter("camera_matrix").get_parameter_value().double_array_value
        dist_coeffs_list = self.get_parameter("dist_coeffs").get_parameter_value().double_array_value
        
        if len(camera_matrix_flat) == 9:
            self.camera_matrix = np.array(camera_matrix_flat).reshape(3, 3)
        else:
            # Default camera matrix (you should calibrate your camera and set these values)
            self.get_logger().warn("Using default camera matrix. Please calibrate your camera!")
            self.camera_matrix = np.array([
                [800.0, 0.0, 320.0],
                [0.0, 800.0, 240.0],
                [0.0, 0.0, 1.0]
            ])
        
        if len(dist_coeffs_list) > 0:
            self.dist_coeffs = np.array(dist_coeffs_list)
        else:
            self.dist_coeffs = np.zeros((5,))

        # ArUco objects
        self.aruco_dict = get_aruco_dictionary(dict_name)
        self.detector_params = get_aruco_detector_params()

        # Build a detector that works across OpenCV versions
        if hasattr(cv2.aruco, "ArucoDetector"):
            self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, cv2.aruco.DetectorParameters())
        else:
            self.detector = None  # we'll call detectMarkers with legacy API

        # Bridge and QoS
        self.bridge = CvBridge()
        qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
        )

        # Subscription
        self.image_sub = self.create_subscription(
            Image,
            topic,
            self.image_callback,
            10
        )
        
        # Publisher for marker poses
        self.pose_pub = self.create_publisher(
            PoseStamped,
            '/aruco_pose',
            10
        )
        
        self.get_logger().info(f"Listening on {topic}, dictionary={dict_name}")
        self.get_logger().info(f"Publishing poses to /aruco_pose")

    def image_callback(self, msg: Image):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding=self.desired_encoding)
        except CvBridgeError as e:
            self.get_logger().warn(f"cv_bridge error: {e}")
            return
        if frame is None:
            return

        # Detection (works with both newer and older OpenCV APIs)
        if self.detector is not None:
            corners, ids, _ = self.detector.detectMarkers(frame)
        else:
            corners, ids, _ = cv2.aruco.detectMarkers(
                frame, self.aruco_dict, parameters=self.detector_params
            )

        if ids is not None and len(ids) > 0:
            ids_flat = ids.flatten().tolist()
            
            # Estimate pose for each marker
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, 
                self.marker_size, 
                self.camera_matrix, 
                self.dist_coeffs
            )
            
            for i, marker_id in enumerate(ids_flat):
                # Get rotation and translation vectors
                rvec = rvecs[i][0]
                tvec = tvecs[i][0]
                
                # Convert rotation vector to rotation matrix
                rotation_matrix, _ = cv2.Rodrigues(rvec)
                
                # Convert rotation matrix to quaternion using scipy
                r = Rotation.from_matrix(rotation_matrix)
                quat = r.as_quat()  # Returns [x, y, z, w]
                
                # Create and publish PoseStamped message
                pose_msg = PoseStamped()
                pose_msg.header.stamp = msg.header.stamp
                pose_msg.header.frame_id = msg.header.frame_id if msg.header.frame_id else "camera_frame"
                
                # Position
                pose_msg.pose.position.x = float(tvec[0])
                pose_msg.pose.position.y = float(tvec[1])
                pose_msg.pose.position.z = float(tvec[2])
                
                # Orientation (quaternion)
                pose_msg.pose.orientation.x = float(quat[0])
                pose_msg.pose.orientation.y = float(quat[1])
                pose_msg.pose.orientation.z = float(quat[2])
                pose_msg.pose.orientation.w = float(quat[3])
                
                self.pose_pub.publish(pose_msg)
                
                self.get_logger().info(
                    f"Marker ID {marker_id}: "
                    f"Pos=[{tvec[0]:.3f}, {tvec[1]:.3f}, {tvec[2]:.3f}]m, "
                    f"Quat=[{quat[0]:.3f}, {quat[1]:.3f}, {quat[2]:.3f}, {quat[3]:.3f}]"
                )
        else:
            self.get_logger().debug("No markers")

def main():
    rclpy.init()
    node = ArucoDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

# ros2 topic echo /aruco_pose

# Better: check if images are being published
# ros2 topic hz /camera/camera/color/image_raw