import rclpy
from rclpy.node import Node
from yhs_can_interfaces.msg import CtrlCmd
import time

rclpy.init()
node = Node('test_ctrl_cmd')
pub = node.create_publisher(CtrlCmd, 'ctrl_cmd', 10)
msg = CtrlCmd()
msg.ctrl_cmd_velocity = 1.0  # m/s
msg.ctrl_cmd_steering = 0.0  # radians
msg.ctrl_cmd_gear = 1        # e.g., forward
msg.ctrl_cmd_brake = 0
pub.publish(msg)
rclpy.spin_once(node, timeout_sec=0.1)  # Allow time for the message to be sent
# or: time.sleep(0.1)