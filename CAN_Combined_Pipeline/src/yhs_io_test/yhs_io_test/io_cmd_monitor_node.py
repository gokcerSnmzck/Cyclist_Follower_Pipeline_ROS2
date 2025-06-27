#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from yhs_can_interfaces.msg import IoCmd


class IoCmdMonitorNode(Node):
    """
    Monitor node for yhs_can_interfaces/msg/IoCmd
    
    This node subscribes to IoCmd messages and displays their contents.
    """
    
    def __init__(self):
        super().__init__('io_cmd_monitor_node')
        
        # Create subscriber for IoCmd messages
        self.io_cmd_subscription = self.create_subscription(
            IoCmd,
            'io_cmd',
            self.io_cmd_callback,
            10
        )
        
        self.message_count = 0
        
        self.get_logger().info('IoCmd Monitor Node started!')
        self.get_logger().info('Listening for IoCmd messages on topic: io_cmd')
        self.get_logger().info('Turn lamp values: 0=off, 1=left, 2=right')
        
    def io_cmd_callback(self, msg):
        """Callback function for IoCmd messages"""
        self.message_count += 1
        
        # Convert turn lamp value to readable string
        turn_lamp_str = {
            0: "OFF",
            1: "LEFT", 
            2: "RIGHT"
        }.get(msg.io_cmd_turn_lamp, f"UNKNOWN({msg.io_cmd_turn_lamp})")
        
        # Log the received message
        self.get_logger().info(
            f'[{self.message_count:04d}] IoCmd received: '
            f'Enable={msg.io_cmd_enable}, '
            f'Headlamp={msg.io_cmd_upper_beam_headlamp}, '
            f'Turn={turn_lamp_str}, '
            f'Speaker={msg.io_cmd_speaker}'
        )
        
        # Print detailed breakdown
        print(f"\n--- IoCmd Message #{self.message_count} ---")
        print(f"io_cmd_enable: {msg.io_cmd_enable}")
        print(f"io_cmd_upper_beam_headlamp: {msg.io_cmd_upper_beam_headlamp}")
        print(f"io_cmd_turn_lamp: {msg.io_cmd_turn_lamp} ({turn_lamp_str})")
        print(f"io_cmd_speaker: {msg.io_cmd_speaker}")
        print("-" * 35)


def main(args=None):
    rclpy.init(args=args)
    
    node = IoCmdMonitorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down IoCmd Monitor Node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
