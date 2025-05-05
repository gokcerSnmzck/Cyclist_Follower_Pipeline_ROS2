from setuptools import setup

package_name = 'ros2_deepstream_json_node'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gokcer',
    maintainer_email='your_email@example.com',
    description='ROS2 node for DeepStream that publishes detection metadata as JSON',
    license='MIT',
    entry_points={
        'console_scripts': [
            'ros2_deepstream_json_node = ros2_deepstream_json_node.ros2_deepstream_json_node:main',
        ],
    },
)
