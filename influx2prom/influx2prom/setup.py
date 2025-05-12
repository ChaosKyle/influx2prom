from setuptools import setup, find_packages

setup(
    name="influx2prom",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "influx2prom=src.main:main",
        ],
    },
    python_requires=">=3.6",
    description="Convert InfluxDB data to Prometheus format",
    author="Chaoskyle",
    author_email="chaoskyle@example.com",
    url="https://github.com/chaoskyle/influx2prom",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)