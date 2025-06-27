from setuptools import setup

package_name = 'hybrid_reid_ros_node'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'opencv-python', 'numpy', 'scipy'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='ROS2 wrapper for Hybrid ReID tracker',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hybrid_reid_ros_node = hybrid_reid_ros_node.hybrid_reid_ros_node:main',
        ],
    },
)
