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

import time
from unittest import mock

import pycf3

import pytest


# =============================================================================
# CACHE TEST
# =============================================================================


def test_cache_same_call(cf3_temp_cache, load_mresponse):
    cf3 = cf3_temp_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse) as get:
        with pytest.deprecated_call():
            cf3.equatorial_search(distance=10)
            cf3.equatorial_search(distance=10)

    get.assert_called_once()
    assert len(cf3.cache) == 1


def test_cache_two_call(cf3_temp_cache, load_mresponse):
    cf3 = cf3_temp_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse) as get:
        with pytest.deprecated_call():
            cf3.equatorial_search(distance=10)
            cf3.equatorial_search(velocity=10)

    assert get.call_count == 2
    assert len(cf3.cache) == 2


def test_no_cache(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    assert len(cf3.cache) == 0
    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse) as get:
        with pytest.deprecated_call():
            cf3.equatorial_search(distance=10)
            cf3.equatorial_search(velocity=10)

    assert get.call_count == 2
    assert len(cf3.cache) == 0


def test_cache_expire(tmp_cache, load_mresponse):
    cache = tmp_cache

    cf3 = pycf3.CF3(cache=cache, cache_expire=2)

    assert len(cache) == 0
    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse) as get:
        with pytest.deprecated_call():
            cf3.equatorial_search(distance=10)
            time.sleep(3)
            cf3.equatorial_search(velocity=10)

    assert get.call_count == 2
    assert len(cache) == 1
