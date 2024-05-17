from setuptools import find_packages, setup

package_name = 'lidar'

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
    maintainer='hvalborg',
    maintainer_email='hvalborg@todo.todo',
    description='TODO: LiDAR measurement',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
         	'talker = lidar.publisher3:main',
            'test_sens = lidar.publisher4:main',
            'center_pub = lidar.center_pub:main',
            'focus_pub = lidar.focus_pub:main',
            'listener = lidar.subscriber:main',
        ],
    },
)
