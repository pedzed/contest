from setuptools import setup
from setuptools import find_packages

setup(
    name="ConTest Library",
    packages=find_packages(),
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest",
    ],
)
