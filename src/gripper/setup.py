from setuptools import find_packages, setup
package_name = 'gripper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 👇 add this line
        ('share/' + package_name + '/launch', ['launch/gripper_bringup.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ryanl',
    maintainer_email='z5422416@ad.unsw.edu.au',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gripper_bridge = gripper.gripper_bridge_node:main'
        ],
    },
)
