import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/gokcer/my_nodes_project/install/deepstream_ros_node_json'
