#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Header
from geometry_msgs.msg import Point

from detection_msgs.msg import Detection2DArray, Detection2D, BoundingBox2D
from zed_msgs.msg import ObjectsStamped, Object

class TestDetectionPublisher(Node):
    def __init__(self):
        super().__init__('test_detection_publisher')
        self.get_logger().info("TestDetectionPublisher started.")

        self.ds_pub = self.create_publisher(Detection2DArray, '/deepstream/detections', 10)
        self.zed_pub = self.create_publisher(ObjectsStamped, '/zed2i/obj_det/objects', 10)

        self.timer = self.create_timer(1.0, self.publish_fake_data)
        self.tracking_id = 1

        # Camera intrinsics (match fusion node)
        self.fx = 525.0
        self.fy = 525.0
        self.cx = 640.0 / 2
        self.cy = 480.0 / 2

    def publish_fake_data(self):
        now = self.get_clock().now().to_msg()

        # Target 2D center in DeepStream
        center_u = 350
        center_v = 300

        # Choose Z distance and back-calculate (x, y) from 2D projection
        z = 5.0
        x = ((center_u - self.cx) * z) / self.fx
        y = ((center_v - self.cy) * z) / self.fy

        # Log projection values
        self.get_logger().info(f"Simulated 3D ZED position: x={x:.2f}, y={y:.2f}, z={z:.2f}")

        # ---- Fake DeepStream detection ----
        bbox = BoundingBox2D()
        bbox.x = center_u - 50.0
        bbox.y = center_v - 100.0
        bbox.width = 100.0
        bbox.height = 200.0

        det = Detection2D()
        det.tracking_id = self.tracking_id
        det.class_id = 0
        det.label = "person"
        det.confidence = 0.95
        det.bbox = bbox

        det_array = Detection2DArray()
        det_array.header = Header(stamp=now, frame_id="zed2i_left_camera_frame")
        det_array.detections.append(det)
        self.ds_pub.publish(det_array)

        self.get_logger().info("Published DeepStream detection.")

        # ---- Fake ZED object ----
        obj = Object()
        obj.label_id = 0
        obj.label = "person"
        obj.confidence = 90.0
        obj.position = [x, y, z]

        zed_msg = ObjectsStamped()
        zed_msg.header = Header(stamp=now, frame_id="zed2i_left_camera_frame")
        zed_msg.objects.append(obj)
        self.zed_pub.publish(zed_msg)

        self.get_logger().info("Published ZED 3D object.")


def main(args=None):
    rclpy.init(args=args)
    node = TestDetectionPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
