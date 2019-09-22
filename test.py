#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/pycf3/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Test for Python client for Cosmicflows-3 Distance-Velocity Calculator at
distances less than 400 Mpc (http://edd.ifa.hawaii.edu/CF3calculator/)

"""


# =============================================================================
# IMPORTS
# =============================================================================

import pickle
from unittest import mock

import pycf3


# =============================================================================
# TESTCASES
# =============================================================================

class TestCaseEquatorial:

    def test_default(self):
        with open("mock_data/tcEquatorial_default.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.equatorial_search()
