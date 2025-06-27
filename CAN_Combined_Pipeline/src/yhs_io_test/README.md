# YHS IoCmd Test Package

This package provides test nodes for the `yhs_can_interfaces/msg/IoCmd` message.

## Message Structure

The `IoCmd` message contains the following fields:
- `io_cmd_enable` (bool): Enable/disable IO commands
- `io_cmd_upper_beam_headlamp` (bool): Control upper beam headlamp
- `io_cmd_turn_lamp` (uint8): Control turn signals
  - `0` = All off
  - `1` = Left turn signal
  - `2` = Right turn signal
- `io_cmd_speaker` (bool): Control speaker

## Available Nodes

### 1. Automatic Test Node (`io_cmd_test`)
Automatically cycles through different test scenarios every 2 seconds.

**Usage:**
```bash
ros2 run yhs_io_test io_cmd_test
```

### 2. Interactive Test Node (`io_cmd_interactive`)
Allows manual control of IoCmd parameters through keyboard input.

**Usage:**
```bash
ros2 run yhs_io_test io_cmd_interactive
```

**Commands:**
- `e` - Toggle io_cmd_enable
- `h` - Toggle io_cmd_upper_beam_headlamp
- `t` - Cycle io_cmd_turn_lamp (0→1→2→0...)
- `s` - Toggle io_cmd_speaker
- `p` - Publish current message
- `r` - Print current state
- `?` - Show help
- `q` - Quit

### 3. Monitor Node (`io_cmd_monitor`)
Subscribes to and displays IoCmd messages.

**Usage:**
```bash
ros2 run yhs_io_test io_cmd_monitor
```

## Example Usage

1. **Terminal 1** - Start the monitor:
```bash
ros2 run yhs_io_test io_cmd_monitor
```

2. **Terminal 2** - Run the automatic test:
```bash
ros2 run yhs_io_test io_cmd_test
```

Or run the interactive test:
```bash
ros2 run yhs_io_test io_cmd_interactive
```

3. **Terminal 3** (optional) - Check the topic:
```bash
ros2 topic echo /io_cmd
```

## Building the Package

```bash
cd ~/ros2_ws
colcon build --packages-select yhs_io_test
source install/setup.bash
```

## Topic Information

All nodes use the topic `/io_cmd` for publishing/subscribing to `IoCmd` messages.

You can also use standard ROS2 tools:
```bash
# Check if the topic exists
ros2 topic list | grep io_cmd

# See the message structure
ros2 interface show yhs_can_interfaces/msg/IoCmd

# Echo messages
ros2 topic echo /io_cmd

# Publish manually
ros2 topic pub /io_cmd yhs_can_interfaces/msg/IoCmd "{io_cmd_enable: true, io_cmd_upper_beam_headlamp: false, io_cmd_turn_lamp: 1, io_cmd_speaker: false}"
```
