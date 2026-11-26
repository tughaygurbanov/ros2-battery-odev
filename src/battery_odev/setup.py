import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'battery_odev'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tughay',
    maintainer_email='tughay.gurbanov@gmail.com',
    description='AUV battery monitoring ROS 2 homework',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'battery_node = battery_odev.battery_node:main',
            'monitor_node = battery_odev.monitor_node:main',
        ],
    },
)