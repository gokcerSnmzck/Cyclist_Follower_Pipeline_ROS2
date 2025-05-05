import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/gokcer/my_nodes_project/install/ros2_deepstream_json_node'
