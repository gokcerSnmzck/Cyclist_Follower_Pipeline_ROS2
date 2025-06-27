from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
import os

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_hybrid = LaunchConfiguration('use_hybrid')

    zed_wrapper_dir = get_package_share_directory('zed_wrapper')
    cmdvel_to_ackermann_dir = get_package_share_directory('cmdvel_to_ackermann')

    # ZED camera
    zed_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(zed_wrapper_dir, 'launch', 'zed_camera.launch.py')
        ),
        launch_arguments={
            'camera_model': 'zed2i',
            'sim_mode': 'true'
        }.items()
    )

    # DeepStream or Hybrid node (after 5s)
    detection_node = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='deepstream_ros_node_json',
                executable='deepstream_ros_node_json',
                name='deepstream_node',
                condition=UnlessCondition(use_hybrid),
                output='screen'
            ),
            Node(
                package='hybrid_reid_ros_node',
                executable='hybrid_reid_ros_node',
                name='hybrid_reid_node',
                condition=IfCondition(use_hybrid),
                output='screen'
            )
        ]
    )

    # Fusion node (after 8s total)
    fusion_node = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='fusion_node',
                executable='fusion_node.py',
                name='fusion_node',
                output='screen'
            )
        ]
    )

    # Person follower and Ackermann nodes (after 10s)
    follower_and_control = TimerAction(
        period=10.0,
        actions=[
            Node(
                package='person_follower_pkg',
                executable='person_follower',
                name='person_follower',
                output='screen'
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(cmdvel_to_ackermann_dir, 'cmdvel_to_ackermann.launch.py')
                ),
                launch_arguments={
                    'acceleration': '0.5',
                    'steering_velocity': '0.5'
                }.items()
            )
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_hybrid',
            default_value='false',
            description='Use hybrid_reid instead of deepstream for detection'
        ),
        zed_launch,
        detection_node,
        fusion_node,
        follower_and_control
    ])

