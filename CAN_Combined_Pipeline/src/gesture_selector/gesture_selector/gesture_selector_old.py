import rclpy
from rclpy.node import Node
from zed_msgs.msg import ObjectsStamped
from std_msgs.msg import Int32
from collections import defaultdict, deque
import numpy as np
import math

WRIST_INDEX = 4        # RIGHT_WRIST
SHOULDER_INDEX = 2     # RIGHT_SHOULDER

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

        self.state = 'IDLE'
        self.state_start_time = self.get_clock().now().nanoseconds / 1e9

        self.motion_history = defaultdict(lambda: deque(maxlen=30))  # Stores (timestamp, wrist_x)
        self.tracked_person_id = None

        self.get_logger().info("Gesture selector node started.")

    def change_state(self, new_state):
        self.get_logger().info(f"State change: {self.state} -> {new_state}")
        self.state = new_state
        self.state_start_time = self.get_clock().now().nanoseconds / 1e9

    def is_waving(self, person_id, current_time):
        history = self.motion_history[person_id]

        # Filter old entries (last 2 seconds)
        recent = [(t, x) for (t, x) in history if current_time - t < 2.0]
        self.motion_history[person_id] = deque(recent, maxlen=30)

        if len(recent) < 5:
            return False

        directions = []
        for i in range(1, len(recent)):
            dx = recent[i][1] - recent[i-1][1]
            if abs(dx) < 0.03:
                continue  # ignore tiny changes
            directions.append(np.sign(dx))

        # Count sign changes
        sign_changes = sum(
            1 for i in range(1, len(directions))
            if directions[i] != directions[i-1]
        )

        self.get_logger().info(f"↔️ Person {person_id} waving sign changes: {sign_changes}")

        return sign_changes >= 3

    def callback(self, msg):
        current_time = self.get_clock().now().nanoseconds / 1e9

        for obj in msg.objects:
            if not obj.skeleton_available:
                continue

            keypoints = obj.skeleton_3d.keypoints
            if len(keypoints) <= max(WRIST_INDEX, SHOULDER_INDEX):
                continue

            wrist = keypoints[WRIST_INDEX].kp
            shoulder = keypoints[SHOULDER_INDEX].kp

            if any(math.isnan(val) for val in wrist + shoulder):
                continue

            person_id = obj.label_id

            wrist_x = wrist[0]
            wrist_y = wrist[1]
            shoulder_y = shoulder[1]

            # # --- Debugging ---
            # self.get_logger().info(
            #     f"Person {person_id} — Wrist Y: {wrist_y:.2f}, Shoulder Y: {shoulder_y:.2f}, Wrist X: {wrist_x:.2f}"
            # )

            if self.state == 'IDLE':
                # Check for hand raised
                if wrist_y > shoulder_y + 0.1:
                    self.get_logger().info(f"🙋 Person {person_id} raised hand.")
                    self.tracked_person_id = person_id
                    self.change_state('HAND_RAISED')
                    self.motion_history[person_id].clear()

            elif self.state == 'HAND_RAISED' and person_id == self.tracked_person_id:
                self.motion_history[person_id].append((current_time, wrist_x))

                if current_time - self.state_start_time > 3.0:
                    self.get_logger().info("⏱️ Timeout: No waving detected.")
                    self.change_state('IDLE')
                    self.tracked_person_id = None
                    continue

                if self.is_waving(person_id, current_time):
                    self.get_logger().info(f"✅ Waving gesture detected from person {person_id}")
                    self.publisher.publish(Int32(data=person_id))
                    self.change_state('SELECTED')
                    break

            elif self.state == 'SELECTED':
                # Do nothing, already selected
                pass

def main(args=None):
    rclpy.init(args=args)
    node = GestureSelector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
