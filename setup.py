#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: setup.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This file is used to create the package we'll publish to PyPI.
"""

import importlib.util
import os
from pathlib import Path
from setuptools import setup, find_packages
from codecs import open  # Use a consistent encoding.
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get the base version from the library.  (We'll find it in the `version.py`
# file in the src directory, but we'll bypass actually loading up the library.)
vspec = importlib.util.spec_from_file_location(
  "version",
  str(Path(__file__).resolve().parent /
      'jccli'/"version.py")
)
vmod = importlib.util.module_from_spec(vspec)
vspec.loader.exec_module(vmod)
version = getattr(vmod, '__version__')

# If the environment has a build number set...
if os.getenv('buildnum') is not None:
    # ...append it to the version.
    version = "{version}.{buildnum}".format(
        version=version,
        buildnum=os.getenv('buildnum')
    )

install_requirements = [
    "click>=7.0,<8",
    "jcapiv1 @ https://github.com/TheJumpCloud/jcapi-python/archive/v3.3.0.zip#subdirectory=jcapiv1",
    "jcapiv2 @ https://github.com/TheJumpCloud/jcapi-python/archive/v3.3.0.zip#subdirectory=jcapiv2",
    "PyYaml>=5.1,<6.0"
]

setup(
    name='jccli',
    description="A Jumpcloud command line client",
    long_description=long_description,
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=version,
    python_requires=">=3",
    install_requires=install_requirements,
    entry_points={
        "console_scripts": [
            'jccli = jccli.cli:cli'
        ]
    },
    license='Apache Software License',  # noqa
    author='zaro0508',
    author_email='zaro0508@gmail.com',
    # Use the URL to the github repo.
    url= 'https://github.com/Sage-Bionetworks/jccli',
    download_url=(
        f'https://github.com/Sage-Bionetworks/'
        f'jccli/archive/{version}.tar.gz'
    ),
    keywords=[
        "jccli",
        "jumpcloud",
        "cli"
    ],
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',

      # Indicate who your project is intended for.
      'Intended Audience :: Developers',
      'Natural Language :: English',
      'Environment :: Console',

        # Pick your license.  (It should match "license" above.)
        # noqa
        'License :: OSI Approved :: Apache Software License',
        # noqa

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True
)
