#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from typing import Optional, Dict

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

        dict_name = self.get_parameter("dictionary").get_parameter_value().string_value
        topic = self.get_parameter("topic").get_parameter_value().string_value
        self.desired_encoding = self.get_parameter("desired_encoding").get_parameter_value().string_value

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
        self.sub = self.create_subscription(Image, topic, self.image_cb, qos)
        self.get_logger().info(f"Listening on {topic}, dictionary={dict_name}")

    def image_cb(self, msg: Image):
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
            self.get_logger().info(
                f"Detected {len(ids_flat)} marker(s): {ids_flat}"
            )
            # If you also want corners, uncomment:
            # for i, c in zip(ids_flat, corners):
            #     self.get_logger().info(f"ID {i} corners (px): {np.round(c[0],1).tolist()}")
        else:
            # Uncomment if you want a heartbeat with no detections:
            self.get_logger().debug("No markers")
            pass

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
