from setuptools import setup

package_name = 'gripper'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],                   # <-- must match the Python package dir "gripper/"
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),  # <— critical
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/gripper_bridge.launch.py']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='You',
    maintainer_email='you@example.com',
    description='Serial gripper action bridge',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'gripper_bridge_node = gripper.gripper_bridge_node:main',
        ],
    },
)
