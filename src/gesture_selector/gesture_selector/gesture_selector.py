import rclpy
from rclpy.node import Node
from zed_msgs.msg import ObjectsStamped
from std_msgs.msg import Int32
from collections import defaultdict, deque
import numpy as np
import math

WRIST_INDEX = 30
SHOULDER_INDEX = 2

class GestureSelector(Node):
    def __init__(self):
        super().__init__('gesture_selector_node')
        self.subscription = self.create_subscription(
            ObjectsStamped,
            '/zed/zed_node/body_trk/skeletons',
            self.callback,
            10
        )
        self.publisher = self.create_publisher(Int32, '/selected_person_id', 10)
        self.motion_history = defaultdict(lambda: deque(maxlen=10))
        self.selected_id = None
        self.get_logger().info("Listening for gestures on /zed/zed_node/body_trk/skeletons")

    def callback(self, msg):
        if self.selected_id is not None:
            return

        for obj in msg.objects:
            if not obj.skeleton_available:
                continue

            keypoints = obj.skeleton_3d.keypoints
            if len(keypoints) <= max(WRIST_INDEX, SHOULDER_INDEX):
                continue

            wrist = keypoints[WRIST_INDEX].kp
            shoulder = keypoints[SHOULDER_INDEX].kp

            # Validate keypoints
            if any(math.isnan(val) for val in wrist + shoulder):
                continue

            person_id = obj.label_id

            # Check if hand is raised above shoulder
            if wrist[1] > shoulder[1]:
                self.motion_history[person_id].append(wrist[0])
                history = self.motion_history[person_id]

                if len(history) >= 5:
                    stddev = np.std(history)
                    self.get_logger().info(f"ID {person_id} stddev: {stddev:.4f}")

                    if stddev > 0.03:  # Waving detected
                        self.get_logger().info(f"✅ Selected person ID: {person_id}")
                        self.selected_id = person_id
                        self.publisher.publish(Int32(data=person_id))
                        break

def main(args=None):
    rclpy.init(args=args)
    node = GestureSelector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
