from setuptools import find_packages, setup

package_name = 'py_Driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/hvalborg.launch.py']),
        ('share/' + package_name + '/launch', ['launch/terminal.launch.py']),
        ('share/' + package_name + '/launch', ['launch/terminal2.launch.py']),
        ('share/' + package_name + '/launch', ['launch/timed.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hvalborg2',
    maintainer_email='cs.schulz@live.dk',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wheely = py_Driver.py_wheely:main',
            'controller = py_Driver.wheely:main',
            'single_contr = py_Driver.single_control:main',
            'extra_contr = py_Driver.extra_controller:main',
            'routine = py_Driver.routine:main',
            'test_contr = py_Driver.Test_Controller:main',
        ],
    },
)
