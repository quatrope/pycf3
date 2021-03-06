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
import random
import time

from numpy import testing as npt

import pycf3

import pytest

# =============================================================================
# MARKERS
# =============================================================================

pytestmark = [pytest.mark.integration]


# =============================================================================
# SLEEP BASE
# =============================================================================


def teardown_function(function):
    s = random.random()
    time.sleep(s)


# =============================================================================
# EQUATORIAL TESTCASE
# =============================================================================


def test_equatorial_calculate_velocity_dis_EQ_10(nam_no_cache, load_mresponse):
    nam = nam_no_cache

    result = nam.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)

    assert result.calculator == pycf3.NAM.CALCULATOR
    assert result.url == pycf3.NAM.URL
    assert result.coordinate == pycf3.CoordinateSystem.equatorial
    assert result.calculated_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    npt.assert_array_equal(result.observed_distance_, [10.0])
    npt.assert_almost_equal(
        result.observed_velocity_, 1135.7191488217507, decimal=4
    )

    assert result.adjusted_distance_ is None
    assert result.adjusted_velocity_ is None

    npt.assert_almost_equal(result.alpha, 187.78917, decimal=4)
    npt.assert_almost_equal(result.delta, 13.33386, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


def test_equatorial_calculate_distance_vel_EQ_10(nam_no_cache, load_mresponse):
    nam = nam_no_cache

    result = nam.calculate_distance(ra=187.78917, dec=13.33386, velocity=10)

    assert result.calculator == pycf3.NAM.CALCULATOR
    assert result.url == pycf3.NAM.URL
    assert result.coordinate == pycf3.CoordinateSystem.equatorial
    assert result.calculated_by == pycf3.Parameter.velocity
    assert result.distance is None
    assert result.velocity == 10

    npt.assert_array_equal(result.observed_distance_, [-1000])
    npt.assert_almost_equal(result.observed_velocity_, 10, decimal=4)

    assert result.adjusted_distance_ is None
    assert result.adjusted_velocity_ is None

    npt.assert_almost_equal(result.alpha, 187.78917, decimal=4)
    npt.assert_almost_equal(result.delta, 13.33386, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


# =============================================================================
# GALACTIC TEST CASE
# =============================================================================


def test_galactic_calculate_velocity_dis_EQ_10(nam_no_cache, load_mresponse):
    nam = nam_no_cache

    result = nam.calculate_velocity(glon=282.96547, glat=75.41360, distance=10)

    assert result.calculator == pycf3.NAM.CALCULATOR
    assert result.url == pycf3.NAM.URL
    assert result.coordinate == pycf3.CoordinateSystem.galactic
    assert result.calculated_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    npt.assert_array_equal(result.observed_distance_, [10])
    npt.assert_almost_equal(
        result.observed_velocity_, 1135.7191488217507, decimal=4
    )

    assert result.adjusted_distance_ is None
    assert result.adjusted_velocity_ is None

    npt.assert_almost_equal(result.alpha, 282.96547, decimal=4)
    npt.assert_almost_equal(result.delta, 75.41360, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


def test_galactic_calculate_distance_vel_EQ_10(nam_no_cache, load_mresponse):
    nam = nam_no_cache

    result = nam.calculate_distance(glon=282.96547, glat=75.41360, velocity=10)

    assert result.calculator == pycf3.NAM.CALCULATOR
    assert result.url == pycf3.NAM.URL
    assert result.coordinate == pycf3.CoordinateSystem.galactic
    assert result.calculated_by == pycf3.Parameter.velocity
    assert result.distance is None
    assert result.velocity == 10

    npt.assert_array_equal(result.observed_distance_, [-1000])
    npt.assert_almost_equal(result.observed_velocity_, 10, decimal=4)

    assert result.adjusted_distance_ is None
    assert result.adjusted_velocity_ is None

    npt.assert_almost_equal(result.alpha, 282.96547, decimal=4)
    npt.assert_almost_equal(result.delta, 75.41360, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


# =============================================================================
# SUPER-GALACTIC TEST CASE
# =============================================================================


def test_sgalactic_calculate_velocity_dis_EQ_10(nam_no_cache, load_mresponse):
    nam = nam_no_cache

    result = nam.calculate_velocity(sgl=102.0, sgb=-2.0, distance=10)

    assert result.calculator == pycf3.NAM.CALCULATOR
    assert result.url == pycf3.NAM.URL
    assert result.coordinate == pycf3.CoordinateSystem.supergalactic
    assert result.calculated_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    npt.assert_array_equal(result.observed_distance_, [10])
    npt.assert_almost_equal(
        result.observed_velocity_, 1135.7191488217507, decimal=4
    )

    assert result.adjusted_distance_ is None
    assert result.adjusted_velocity_ is None

    npt.assert_almost_equal(result.alpha, 102, decimal=4)
    npt.assert_almost_equal(result.delta, -2, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


def test_sgalactic_calculate_distance_vel_EQ_10(nam_no_cache, load_mresponse):
    nam = nam_no_cache

    result = nam.calculate_distance(sgl=102.0, sgb=-2.0, velocity=10)

    assert result.calculator == pycf3.NAM.CALCULATOR
    assert result.url == pycf3.NAM.URL
    assert result.coordinate == pycf3.CoordinateSystem.supergalactic
    assert result.calculated_by == pycf3.Parameter.velocity
    assert result.distance is None
    assert result.velocity == 10

    npt.assert_array_equal(result.observed_distance_, [-1000])
    npt.assert_almost_equal(result.observed_velocity_, 10, decimal=4)

    assert result.adjusted_distance_ is None
    assert result.adjusted_velocity_ is None

    npt.assert_almost_equal(result.alpha, 102, decimal=4)
    npt.assert_almost_equal(result.delta, -2, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)
