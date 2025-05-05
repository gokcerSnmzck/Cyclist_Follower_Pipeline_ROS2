import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from detection_msgs.msg import Detection2D, Detection2DArray, BoundingBox2D

import subprocess
import threading
import json
import re


class DeepStreamAppBridge(Node):
    def __init__(self):
        super().__init__('deepstream_ros_node')
        self.publisher = self.create_publisher(Detection2DArray, '/deepstream/detections', 10)
        self.get_logger().info("Starting DeepStream ROS node (deepstream-app bridge)...")

        # Path to your DeepStream app config
        config_path = "/home/gokcer/my_nodes_project/config/deepstream_app_config.txt"

        # Launch deepstream-app as a subprocess
        self.process = subprocess.Popen(
            ["deepstream-app", "-c", config_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Start a thread to stream stdout and extract detections
        self.thread = threading.Thread(target=self.read_and_publish, daemon=True)
        self.thread.start()

    def read_and_publish(self):
        for line in self.process.stdout:
            line = line.strip()
            if not line:
                continue

            json_line = self.extract_json(line)
            if json_line:
                try:
                    data = json.loads(json_line)
                    self.publish_detections_from_json(data)
                except json.JSONDecodeError:
                    self.get_logger().warn("Failed to parse JSON line.")

    def extract_json(self, line):
        # Match JSON anywhere in the line
        match = re.search(r'(\{.*\})', line)
        return match.group(1) if match else None

    def publish_detections_from_json(self, data):
        msg = Detection2DArray()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "deepstream_camera"

        for obj in data.get("objects", []):
            det = Detection2D()
            det.tracking_id = int(obj.get("object_id", 0))
            det.class_id = int(obj.get("class_id", 0))
            det.label = obj.get("label", "unknown")
            det.confidence = float(obj.get("confidence", 0.0))

            bbox_data = obj.get("bbox", {})
            bbox = BoundingBox2D()
            bbox.x = float(bbox_data.get("left", 0.0))
            bbox.y = float(bbox_data.get("top", 0.0))
            bbox.width = float(bbox_data.get("width", 0.0))
            bbox.height = float(bbox_data.get("height", 0.0))
            det.bbox = bbox

            msg.detections.append(det)

        self.publisher.publish(msg)
        self.get_logger().info(f"Published {len(msg.detections)} DeepStream detections.")

    def destroy_node(self):
        self.get_logger().info("Shutting down deepstream-app...")
        if self.process:
            self.process.terminate()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DeepStreamAppBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
