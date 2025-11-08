from setuptools import find_packages
from setuptools import setup

setup(
    name='ur5e_moveit_config_custom',
    version='0.0.1',
    packages=find_packages(
        include=('ur5e_moveit_config_custom', 'ur5e_moveit_config_custom.*')),
)
