"""Setup for the jsonstat-validator package.

This setup script configures the jsonstat-validator package for distribution.
It includes metadata about the package, such as its name, version, author,
description, and dependencies.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jsonstat-validator",
    version="0.1.0",
    author="Ahmed Hassan",
    author_email="ahmedhassan.ahmed@fao.org",
    description="A validator for JSON-stat 2.0 format data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmed-hassan19/jsonstat-validator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: File Formats :: JSON :: JSON-stat",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic==2.*",
    ],
    extras_require={
        "dev": ["pytest>=8.1.1"],
    },
)
