from setuptools import setup

package_name = 'person_follower_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Robot controller node to follow a person using fused_target messages',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'person_follower = person_follower_pkg.person_follower:main',
        ],
    },
)
