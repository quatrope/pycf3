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


# =============================================================================
# CACHE TEST
# =============================================================================


def test_cache_same_call(fakeclient_temp_cache, load_mresponse):
    client = fakeclient_temp_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")

    with mock.patch("requests.Session.get", return_value=mresponse) as get:
        client.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)
        client.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)

    get.assert_called_once()
    assert len(client.cache) == 1


def test_cache_two_call(fakeclient_temp_cache, load_mresponse):
    client = fakeclient_temp_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")

    with mock.patch("requests.Session.get", return_value=mresponse) as get:
        client.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)
        client.calculate_distance(ra=187.78917, dec=13.33386, velocity=10)

    assert get.call_count == 2
    assert len(client.cache) == 2


def test_no_cache(fakeclient_no_cache, load_mresponse):
    client = fakeclient_no_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")

    with mock.patch("requests.Session.get", return_value=mresponse) as get:
        client.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)
        client.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)

    assert get.call_count == 2
    assert len(client.cache) == 0


def test_cache_expire(fakeclient_class, tmp_cache, load_mresponse):
    cache = tmp_cache
    client = fakeclient_class(cache=cache, cache_expire=1)

    assert len(cache) == 0
    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse) as get:
        client.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)
        time.sleep(1.3)
        client.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)

    assert get.call_count == 2
    assert len(cache) == 1
