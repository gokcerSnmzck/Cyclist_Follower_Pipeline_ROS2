from setuptools import setup

package_name = 'deepstream_ros_node_json'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yourname',
    maintainer_email='your@email.com',
    description='ROS 2 node for DeepStream + YOLOv11 object detection',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'deepstream_ros_node_json = deepstream_ros_node_json.deepstream_ros_node_json:main'
        ],
    },
)

