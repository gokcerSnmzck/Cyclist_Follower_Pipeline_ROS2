import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from yhs_can_interfaces.msg import CtrlCmd

class CmdVelToCAN(Node):
    def __init__(self):
        super().__init__('cmdvel_to_can_node')
        self.publisher_ = self.create_publisher(CtrlCmd, 'ctrl_cmd', 10)
        self.subscription = self.create_subscription(
            Twist,
            'cmdvel',
            self.cmdvel_callback,
            10)
        self.get_logger().info('cmdvel_to_can_node started, listening to /cmdvel')

    def cmdvel_callback(self, msg: Twist):
        ctrl_cmd = CtrlCmd()
        ctrl_cmd.ctrl_cmd_velocity = msg.linear.x * 10 # Range 0 to 40 (input range 0 to 0.4)
        ctrl_cmd.ctrl_cmd_steering = msg.angular.z * 40 # Range -32 to 32, where 0 is straight ahead (input range -0.8 to 0.8)       
        ctrl_cmd.ctrl_cmd_gear = 4  # Forward gear -> 4
                                                # 01: P
                                                # 02: R
                                                # 03: N
                                                # 04: D

        if msg.linear.x == 0 and msg.angular.z == 0:
            ctrl_cmd.ctrl_cmd_brake = 1 # Brake engaged
            ctrl_cmd.ctrl_cmd_gear = 3  # Neutral gear -> 3
        else:
            ctrl_cmd.ctrl_cmd_brake = 0 # No brake

        self.publisher_.publish(ctrl_cmd)
        self.get_logger().info(f'Published CtrlCmd: velocity={msg.linear.x}, steering={msg.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelToCAN()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
