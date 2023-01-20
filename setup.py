"""Setup.py script for packaging project."""

from os import getenv
from setuptools import setup

import os

if __name__ == '__main__':
    setup(
        name='reports',
        version=getenv('PACKAGE_VERSION', '1.0.0'),
        package_dir={'': 'src'},
        packages=["reports"],
        description='A demo package for ETL Jobs in Apio TFI Project.'
    )