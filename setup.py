#!/usr/bin/env python3
"""Setup script for HaloOglasi Parser package."""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="halooglasi-parser",
    version="1.0.0",
    author="HaloOglasi Parser Team",
    description="Automated real estate listing parser with Telegram notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/halooglasi-parser",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "halooglasi-search=halooglasi_parser.cli:main",
            "halooglasi-scheduler=halooglasi_parser.scheduler:main",
        ],
    },
    include_package_data=True,
) 