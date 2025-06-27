#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from detection_msgs.msg import TargetPosition
from geometry_msgs.msg import Twist
from builtin_interfaces.msg import Time


class PersonFollower(Node):
    def __init__(self):
        super().__init__('person_follower')
        self.target_sub = self.create_subscription(TargetPosition, '/fused_target', self.target_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Parameters
        self.target_id = None     # Optional: track specific person
        self.min_distance = 1.5   # meters
        self.max_linear_speed = 0.4
        self.max_angular_speed = 0.8
        self.timeout_sec = 1.0    # stop robot if no detection within this time

        self.last_msg_time = self.get_clock().now()
        self.timer = self.create_timer(0.1, self.watchdog_callback)

        self.get_logger().info("PersonFollower node initialized.")

    def target_callback(self, msg: TargetPosition):
        if self.target_id is not None and msg.id != self.target_id:
            return

        x = msg.position.x  # forward/back
        y = msg.position.y  # left/right

        if x <= 0.1:
            self.get_logger().warn("Invalid or too close target position. Skipping.")
            return

        linear = min(self.max_linear_speed, max(0.0, x - self.min_distance))
        angular = max(-self.max_angular_speed, min(self.max_angular_speed, y))

        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular

        self.cmd_pub.publish(twist)
        self.last_msg_time = self.get_clock().now()

        self.get_logger().info(f"Following person ID {msg.id}: linear={linear:.2f} m/s, angular={angular:.2f} rad/s")
        self.get_logger().info(f"Target x={x:.2f}, y={y:.2f}")

    def watchdog_callback(self):
        now = self.get_clock().now()
        if (now - self.last_msg_time) > Duration(seconds=self.timeout_sec):
            twist = Twist()  # zero velocity
            self.cmd_pub.publish(twist)
            self.get_logger().warn("No target detected. Stopping robot.")


def main(args=None):
    rclpy.init(args=args)
    node = PersonFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
