#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/pycf3/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Integration Test for Python client for Cosmicflows-3 Distance-Velocity
Calculator at distances less than 400 Mpc
(http://edd.ifa.hawaii.edu/CF3calculator/)

Warning this code is SLOW!

"""


# =============================================================================
# IMPORTS
# =============================================================================

import random
import time

from numpy import testing as npt

import pycf3

import pytest


# =============================================================================
# MARKERS
# =============================================================================

pytestmark = [pytest.mark.integration, pytest.mark.deprecated_api]


# =============================================================================
# SLEEP BASE
# =============================================================================


def teardown_function(function):
    s = random.random()
    time.sleep(s)


# =============================================================================
# EQUATORIAL TESTCASE
# =============================================================================


def test_integration_equatorial_search(cf3_temp_cache):
    cf3 = cf3_temp_cache

    assert len(cf3.cache) == 0

    with pytest.deprecated_call():
        result = cf3.equatorial_search(distance=10)

    assert len(cf3.cache) == 1

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.equatorial
    assert result.search_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    npt.assert_array_equal(result.observed_distance_, [10.0])
    npt.assert_almost_equal(
        result.observed_velocity_, 730.4691399179898, decimal=4
    )

    npt.assert_array_equal(result.adjusted_distance_, [10.0])
    npt.assert_almost_equal(
        result.adjusted_velocity_, 731.8902182205077, decimal=4
    )

    npt.assert_almost_equal(result.alpha, 187.78917, decimal=4)
    npt.assert_almost_equal(result.delta, 13.33386, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    with pytest.deprecated_call():
        cf3.equatorial_search(distance=10)
    assert len(cf3.cache) == 1

    with pytest.deprecated_call():
        cf3.equatorial_search(distance=11)
    assert len(cf3.cache) == 2


# =============================================================================
# GALACTIC TEST CASE
# =============================================================================


def test_integration_galactic_search(cf3_temp_cache):
    cf3 = cf3_temp_cache

    assert len(cf3.cache) == 0

    with pytest.deprecated_call():
        result = cf3.galactic_search(distance=10)

    assert len(cf3.cache) == 1

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.galactic
    assert result.search_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    npt.assert_array_equal(result.observed_distance_, [10])
    npt.assert_almost_equal(result.observed_velocity_, 730.46917, decimal=4)

    npt.assert_array_equal(result.adjusted_distance_, [10])
    npt.assert_almost_equal(
        result.adjusted_velocity_, 731.89024918019, decimal=4
    )

    npt.assert_almost_equal(result.alpha, 282.96547, decimal=4)
    npt.assert_almost_equal(result.delta, 75.41360, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    with pytest.deprecated_call():
        cf3.galactic_search(distance=10)
    assert len(cf3.cache) == 1

    with pytest.deprecated_call():
        cf3.galactic_search(distance=11)
    assert len(cf3.cache) == 2


# =============================================================================
# SUPER-GALACTIC TEST CASE
# =============================================================================


def test_integration_supergalactic_search(cf3_temp_cache):
    cf3 = cf3_temp_cache

    assert len(cf3.cache) == 0

    with pytest.deprecated_call():
        result = cf3.supergalactic_search(distance=10)

    assert len(cf3.cache) == 1

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.supergalactic
    assert result.search_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    npt.assert_array_equal(result.observed_distance_, [10])
    npt.assert_almost_equal(result.observed_velocity_, 730.46917, decimal=4)

    npt.assert_array_equal(result.adjusted_distance_, [10])
    npt.assert_almost_equal(
        result.adjusted_velocity_, 731.89024918019, decimal=4
    )

    npt.assert_almost_equal(result.alpha, 102, decimal=4)
    npt.assert_almost_equal(result.delta, -2, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    with pytest.deprecated_call():
        cf3.supergalactic_search(distance=10)
    assert len(cf3.cache) == 1

    with pytest.deprecated_call():
        cf3.supergalactic_search(distance=11)
    assert len(cf3.cache) == 2
