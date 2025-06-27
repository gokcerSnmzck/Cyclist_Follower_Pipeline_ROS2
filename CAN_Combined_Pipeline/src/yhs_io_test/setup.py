from setuptools import find_packages, setup

package_name = 'yhs_io_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yuhesen',
    maintainer_email='yuhesen@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'io_cmd_test = yhs_io_test.io_cmd_test_node:main',
            'io_cmd_interactive = yhs_io_test.io_cmd_interactive_node:main',
            'io_cmd_monitor = yhs_io_test.io_cmd_monitor_node:main',
        ],
    },
)
