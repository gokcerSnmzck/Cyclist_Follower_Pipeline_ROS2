from setuptools import setup

package_name = 'trajectory_follower'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Robot controller node to follow a trajectory using fused_target messages',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'trajectory_follower = trajectory_follower.trajectory_follower:main',
        ],
    },
)
