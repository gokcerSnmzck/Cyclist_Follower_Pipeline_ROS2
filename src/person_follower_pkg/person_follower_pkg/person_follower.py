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
        self.target_id = None
        self.min_distance = 1.5
        self.max_linear_speed = 0.4
        self.max_angular_speed = 0.8
        self.timeout_sec = 1.0

        self.last_msg_time = self.get_clock().now()
        self.target_lost = True
        self.timer = self.create_timer(0.1, self.watchdog_callback)

        self.get_logger().info("PersonFollower node initialized.")

    def target_callback(self, msg: TargetPosition):
        if self.target_id is not None and msg.id != self.target_id:
            return

        x = msg.position.x
        y = msg.position.y

        if x <= 0.1:
            self.get_logger().warn("Invalid or too close target position. Skipping.")
            return

        linear = min(self.max_linear_speed, max(0.0, x - self.min_distance))
        angular = max(-self.max_angular_speed, min(self.max_angular_speed, y))

        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.cmd_pub.publish(twist)

        now = self.get_clock().now()
        if self.target_lost:
            self.get_logger().info("Target reacquired. Resuming following.")
            self.target_lost = False
        self.last_msg_time = now

        self.get_logger().info(f"Following person ID {msg.id}: linear={linear:.2f} m/s, angular={angular:.2f} rad/s")

    def watchdog_callback(self):
        now = self.get_clock().now()
        if (now - self.last_msg_time).nanoseconds > int(self.timeout_sec * 1e9):
            if not self.target_lost:
                self.get_logger().warn("Target lost. Stopping robot.")
                self.target_lost = True
                self.cmd_pub.publish(Twist())  # Stop

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
