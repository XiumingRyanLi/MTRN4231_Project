from setuptools import find_packages
from setuptools import setup

setup(
    name='chess_arm_executor',
    version='0.0.2',
    packages=find_packages(
        include=('chess_arm_executor', 'chess_arm_executor.*')),
)
