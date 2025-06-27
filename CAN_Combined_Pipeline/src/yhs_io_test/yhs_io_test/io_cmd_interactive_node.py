#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from yhs_can_interfaces.msg import IoCmd
import threading
import sys


class IoCmdInteractiveNode(Node):
    """
    Interactive test node for yhs_can_interfaces/msg/IoCmd
    
    This node allows manual control of IoCmd parameters through keyboard input.
    """
    
    def __init__(self):
        super().__init__('io_cmd_interactive_node')
        
        # Create publisher for IoCmd messages
        self.io_cmd_publisher = self.create_publisher(
            IoCmd,
            'io_cmd',
            10
        )
        
        # Current message state
        self.current_msg = IoCmd()
        self.current_msg.io_cmd_enable = False
        self.current_msg.io_cmd_upper_beam_headlamp = False
        self.current_msg.io_cmd_turn_lamp = 0
        self.current_msg.io_cmd_speaker = False
        
        self.get_logger().info('IoCmd Interactive Test Node started!')
        self.get_logger().info('Publishing IoCmd messages on topic: io_cmd')
        self.print_help()
        
        # Start keyboard input thread
        self.input_thread = threading.Thread(target=self.keyboard_input_loop, daemon=True)
        self.input_thread.start()
        
    def print_help(self):
        """Print available commands"""
        print("\n" + "="*60)
        print("IoCmd Interactive Control")
        print("="*60)
        print("Commands:")
        print("  e - Toggle io_cmd_enable")
        print("  h - Toggle io_cmd_upper_beam_headlamp")
        print("  t - Cycle io_cmd_turn_lamp (0=off, 1=left, 2=right)")
        print("  s - Toggle io_cmd_speaker")
        print("  p - Publish current message")
        print("  r - Print current state")
        print("  ? - Show this help")
        print("  q - Quit")
        print("="*60)
        self.print_current_state()
        
    def print_current_state(self):
        """Print current message state"""
        turn_lamp_str = {0: "OFF", 1: "LEFT", 2: "RIGHT"}.get(self.current_msg.io_cmd_turn_lamp, "UNKNOWN")
        print(f"\nCurrent State:")
        print(f"  Enable: {self.current_msg.io_cmd_enable}")
        print(f"  Upper Beam Headlamp: {self.current_msg.io_cmd_upper_beam_headlamp}")
        print(f"  Turn Lamp: {self.current_msg.io_cmd_turn_lamp} ({turn_lamp_str})")
        print(f"  Speaker: {self.current_msg.io_cmd_speaker}")
        print("Enter command (? for help): ", end="", flush=True)
        
    def publish_current_message(self):
        """Publish the current message"""
        self.io_cmd_publisher.publish(self.current_msg)
        self.get_logger().info(f'Published: Enable={self.current_msg.io_cmd_enable}, '
                              f'Headlamp={self.current_msg.io_cmd_upper_beam_headlamp}, '
                              f'Turn={self.current_msg.io_cmd_turn_lamp}, '
                              f'Speaker={self.current_msg.io_cmd_speaker}')
        
    def keyboard_input_loop(self):
        """Handle keyboard input in a separate thread"""
        while rclpy.ok():
            try:
                command = input().strip().lower()
                
                if command == 'q':
                    self.get_logger().info('Quitting...')
                    rclpy.shutdown()
                    break
                    
                elif command == 'e':
                    self.current_msg.io_cmd_enable = not self.current_msg.io_cmd_enable
                    print(f"Enable toggled to: {self.current_msg.io_cmd_enable}")
                    
                elif command == 'h':
                    self.current_msg.io_cmd_upper_beam_headlamp = not self.current_msg.io_cmd_upper_beam_headlamp
                    print(f"Upper beam headlamp toggled to: {self.current_msg.io_cmd_upper_beam_headlamp}")
                    
                elif command == 't':
                    self.current_msg.io_cmd_turn_lamp = (self.current_msg.io_cmd_turn_lamp + 1) % 3
                    turn_lamp_str = {0: "OFF", 1: "LEFT", 2: "RIGHT"}[self.current_msg.io_cmd_turn_lamp]
                    print(f"Turn lamp cycled to: {self.current_msg.io_cmd_turn_lamp} ({turn_lamp_str})")
                    
                elif command == 's':
                    self.current_msg.io_cmd_speaker = not self.current_msg.io_cmd_speaker
                    print(f"Speaker toggled to: {self.current_msg.io_cmd_speaker}")
                    
                elif command == 'p':
                    self.publish_current_message()
                    
                elif command == 'r':
                    self.print_current_state()
                    continue  # Don't print the prompt again
                    
                elif command == '?':
                    self.print_help()
                    continue  # Don't print the prompt again
                    
                else:
                    print(f"Unknown command: {command}. Type '?' for help.")
                    
                print("Enter command (? for help): ", end="", flush=True)
                
            except (EOFError, KeyboardInterrupt):
                self.get_logger().info('Shutting down...')
                rclpy.shutdown()
                break
            except Exception as e:
                print(f"Error: {e}")


def main(args=None):
    rclpy.init(args=args)
    
    node = IoCmdInteractiveNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()


if __name__ == '__main__':
    main()
