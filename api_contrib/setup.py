#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

setup(
    author="",
    author_email="",
    description="Common tools for FastAPI services",
    install_requires=[
        'fastapi>=0.63.0',
        'motor>=2.3.1'
    ],
    include_package_data=True,
    keywords="api_contrib",
    name="api_contrib",
    packages=find_packages(),
    version="0.0.1",
)
