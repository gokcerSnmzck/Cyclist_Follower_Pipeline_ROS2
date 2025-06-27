from setuptools import setup

package_name = 'gesture_selector'

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
    description='Gesture detection for target selection',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gesture_selector = gesture_selector.gesture_selector:main',
        ],
    },
)
