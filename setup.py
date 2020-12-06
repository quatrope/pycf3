#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/pycf3/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""This file is for distribute pycf3

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib

from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup  # noqa


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

REQUIREMENTS = [
    "numpy",
    "requests",
    "tabulate",
    "attrs",
    "diskcache",
    "custom_inherit",
    "Deprecated",
]

with open(PATH / "README.md") as fp:
    LONG_DESCRIPTION = fp.read()

DESCRIPTION = (
    "Cosmicflows Galaxy Distance-Velocity Calculator client for Python"
)

with open(PATH / "pycf3.py") as fp:
    VERSION = (
        [line for line in fp.readlines() if line.startswith("__version__")][0]
        .split("=", 1)[-1]
        .strip()
        .replace('"', "")
    )


# =============================================================================
# FUNCTIONS
# =============================================================================


def do_setup():
    setup(
        name="pycf3",
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author="QuatroPe",
        author_email="jbc.develop@gmail.com",
        url="https://github.com/quatrope/pycf3",
        license="3 Clause BSD",
        keywords=[
            "astronomy",
            "cosmicflow",
            "Distance",
            "Velocity",
            "calculator",
        ],
        classifiers=(
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Scientific/Engineering",
        ),
        py_modules=["pycf3", "ez_setup"],
        install_requires=REQUIREMENTS,
    )


if __name__ == "__main__":
    do_setup()
