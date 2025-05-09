"""Setup script for the package."""
from setuptools import find_packages, setup

setup(
    name="influx2prom",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
)