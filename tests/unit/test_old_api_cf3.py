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

from unittest import mock

from numpy import testing as npt

import pycf3

import pytest


# =============================================================================
# EQUATORIAL TESTCASE
# =============================================================================


def test_equatorial_search_distance_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.equatorial_search(distance=10)

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.equatorial
    assert result.search_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    assert result.json_ == mresponse.json()

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


def test_equatorial_search_velocity_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_velocity_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.equatorial_search(velocity=10)

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.equatorial
    assert result.search_by == pycf3.Parameter.velocity
    assert result.distance is None
    assert result.velocity == 10

    assert result.json_ == mresponse.json()

    npt.assert_array_equal(result.observed_distance_, [-1000])
    npt.assert_almost_equal(result.observed_velocity_, 10, decimal=4)

    npt.assert_array_equal(result.adjusted_distance_, [-1000])
    npt.assert_almost_equal(result.adjusted_velocity_, 10, decimal=4)

    npt.assert_almost_equal(result.alpha, 187.78917, decimal=4)
    npt.assert_almost_equal(result.delta, 13.33386, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


def test_equatorial_search_ra_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.equatorial_search(ra="foo")


def test_equatorial_search_dec_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.equatorial_search(dec="foo")


def test_equatorial_search_dec_lt_m90(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.equatorial_search(dec=-91)


def test_equatorial_search_dec_gt_90(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.equatorial_search(dec=91)


def test_equatorial_search_distance_velocity_together(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.equatorial_search(distance=10, velocity=10)


def test_equatorial_search_distance_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.equatorial_search(distance="foo")


def test_equatorial_search_velocity_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.equatorial_search(distance="foo")


# =============================================================================
# GALACTIC TEST CASE
# =============================================================================


def test_galactic_search_distance_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcGalactic_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.galactic_search(distance=10)

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.galactic
    assert result.search_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    assert result.json_ == mresponse.json()

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


def test_galactic_search_velocity_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcGalactic_velocity_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.galactic_search(velocity=10)

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.galactic
    assert result.search_by == pycf3.Parameter.velocity
    assert result.distance is None
    assert result.velocity == 10

    assert result.json_ == mresponse.json()

    npt.assert_array_equal(result.observed_distance_, [-1000])
    npt.assert_almost_equal(result.observed_velocity_, 10, decimal=4)

    npt.assert_array_equal(result.adjusted_distance_, [-1000])
    npt.assert_almost_equal(result.adjusted_velocity_, 10, decimal=4)

    npt.assert_almost_equal(result.alpha, 282.96547, decimal=4)
    npt.assert_almost_equal(result.delta, 75.41360, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


def test_galactic_search_glon_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.galactic_search(glon="foo")


def test_galactic_search_glat_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.galactic_search(glat="foo")


def test_galactic_search_glat_lt_m90(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.galactic_search(glat=-91)


def test_galactic_search_glat_gt_90(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.galactic_search(glat=91)


def test_galactic_search_distance_velocity_together(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.galactic_search(distance=10, velocity=10)


def test_galactic_search_distance_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.galactic_search(distance="foo")


def test_galactic_search_velocity_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.galactic_search(distance="foo")


# =============================================================================
# SUPER-GALACTIC TEST CASE
# =============================================================================


def test_supergalactic_search_distance_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcSuperGalactic_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.supergalactic_search(distance=10)

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.supergalactic
    assert result.search_by == pycf3.Parameter.distance
    assert result.distance == 10
    assert result.velocity is None

    assert result.json_ == mresponse.json()

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


def test_supergalactic_search_velocity_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcSuperGalactic_velocity_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.supergalactic_search(velocity=10)

    assert result.calculator == pycf3.CF3.CALCULATOR
    assert result.url == pycf3.CF3.URL
    assert result.coordinate == pycf3.CoordinateSystem.supergalactic
    assert result.search_by == pycf3.Parameter.velocity
    assert result.distance is None
    assert result.velocity == 10

    assert result.json_ == mresponse.json()

    npt.assert_array_equal(result.observed_distance_, [-1000])
    npt.assert_almost_equal(result.observed_velocity_, 10, decimal=4)

    npt.assert_array_equal(result.adjusted_distance_, [-1000])
    npt.assert_almost_equal(result.adjusted_velocity_, 10, decimal=4)

    npt.assert_almost_equal(result.alpha, 102, decimal=4)
    npt.assert_almost_equal(result.delta, -2, decimal=4)

    npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
    npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
    npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
    npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
    npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


def test_supergalactic_search_sgl_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.supergalactic_search(sgl="foo")


def test_supergalactic_search_sgb_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.supergalactic_search(sgb="foo")


def test_supergalactic_search_sgb_lt_m90(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.supergalactic_search(sgb=-91)


def test_supergalactic_search_sgb_gt_90(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.supergalactic_search(sgb=91)


def test_supergalactic_search_distance_velocity_together(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.supergalactic_search(distance=10, velocity=10)


def test_supergalactic_search_distance_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.supergalactic_search(distance="foo")


def test_supergalactic_search_velocity_not_number(cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.supergalactic_search(distance="foo")
