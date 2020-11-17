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

import itertools as it
from unittest import mock

from numpy import testing as npt

import pycf3

import pytest

# =============================================================================
# MARKERS
# =============================================================================

pytestmark = [pytest.mark.xfail]


# =============================================================================
# EQUATORIAL TESTCASE
# =============================================================================


def test_equatorial_calculate_velocity_dis_EQ_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.calculate_velocity(
            ra=187.78917, dec=13.33386, distance=10
        )

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


def test_equatorial_calculate_distance_vel_EQ_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcEquatorial_velocity_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.calculate_distance(
            ra=187.78917, dec=13.33386, velocity=10
        )

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


# =============================================================================
# GALACTIC TEST CASE
# =============================================================================


def test_galactic_calculate_velocity_dis_EQ_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcGalactic_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.calculate_velocity(
            glon=282.96547, glat=75.41360, distance=10
        )

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


def test_galactic_calculate_distance_vel_EQ_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcGalactic_velocity_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.calculate_distance(
            glon=282.96547, glat=75.41360, velocity=10
        )

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


# =============================================================================
# SUPER-GALACTIC TEST CASE
# =============================================================================


def test_sgalactic_calculate_velocity_dis_EQ_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcSuperGalactic_distance_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.calculate_velocity(sgl=102.0, sgb=-2.0, distance=10)

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


def test_sgalactic_calculate_distance_vel_EQ_10(cf3_no_cache, load_mresponse):
    cf3 = cf3_no_cache

    mresponse = load_mresponse("cf3", "tcSuperGalactic_velocity_10.pkl")
    with mock.patch("requests.Session.get", return_value=mresponse):
        result = cf3.calculate_distance(sgl=102.0, sgb=-2.0, velocity=10)

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


# =============================================================================
# calculate_distance with NAN 0 or -
# =============================================================================


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_distance_velocity_eq_0(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.calculate_distance(velocity=0, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_distance_velocity_lt_0(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.calculate_distance(velocity=-1, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_distance_velocity_not_number(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.calculate_distance(velocity="invalid", **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": "invalid"},
        {"glon": 282.96547, "glat": "invalid"},
        {"sgl": 102.0, "sgb": "invalid"},
    ],
)
def test_calculate_distance_delta_not_number(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.calculate_distance(velocity="invalid", **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": "invalid", "dec": 13.33386},
        {"glon": "invalid", "glat": 75.4136},
        {"sgl": "invalid", "sgb": -2.0},
    ],
)
def test_calculate_distance_alpha_not_number(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.calculate_distance(velocity=10, **params)


# =============================================================================
# calculate_distance BAD COORDINATES
# =============================================================================


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 91, "dec": 13.33386},
        {"glon": 91, "glat": 75.4136},
        {"sgl": 91, "sgb": -2.0},
    ],
)
def test_calculate_distance_alpha_gt_90(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.calculate_distance(velocity=10 ** params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": -91, "dec": 13.33386},
        {"glon": -91, "glat": 75.4136},
        {"sgl": -91, "sgb": -2.0},
    ],
)
def test_calculate_distance_alpha_lt_m90(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.calculate_distance(velocity=10 ** params)


# =============================================================================
# calculate_velocity with NAN 0 or -
# =============================================================================


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_velocity_distance_eq_0(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.calculate_velocity(distance=0, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_velocity_distance_lt_0(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.calculate_velocity(distance=-1, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_velocity_distance_not_number(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.calculate_velocity(distance="invalid", **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": "invalid", "dec": 13.33386},
        {"glon": "invalid", "glat": 75.4136},
        {"sgl": "invalid", "sgb": -2.0},
    ],
)
def test_calculate_velocity_alpha_not_number(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.calculate_velocity(distance=10, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": "invalid"},
        {"glon": 282.96547, "glat": "invalid"},
        {"sgl": 102.0, "sgb": "invalid"},
    ],
)
def test_calculate_velocity_delta_not_number(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(TypeError):
        cf3.calculate_velocity(distance=10, **params)


# =============================================================================
# calculate_velocity BAD COORDINATES
# =============================================================================


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 91, "dec": 13.33386},
        {"glon": 91, "glat": 75.4136},
        {"sgl": 91, "sgb": -2.0},
    ],
)
def test_calculate_velocity_alpha_gt_90(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.calculate_velocity(distance=10, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": -91, "dec": 13.33386},
        {"glon": -91, "glat": 75.4136},
        {"sgl": -91, "sgb": -2.0},
    ],
)
def test_calculate_velocity_alpha_lt_m90(params, cf3_no_cache):
    cf3 = cf3_no_cache
    with pytest.raises(ValueError):
        cf3.calculate_velocity(distance=10, **params)


# =============================================================================
# MIX COORDINATES
# =============================================================================


def mix_coordinates():
    for alpha, delta in it.product(pycf3.ALPHA.items(), pycf3.DELTA.items()):
        alpha_system, alpha_name = alpha
        delta_system, delta_name = delta
        if alpha_system != delta_system:
            yield alpha_name, delta_name


@pytest.mark.parametrize("alpha, delta", mix_coordinates())
def test_calculate_velocity_mix_coordinate_system(alpha, delta, cf3_no_cache):
    cf3 = cf3_no_cache
    params = {alpha: 1, delta: 1}
    print(params)
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        cf3.calculate_velocity(distance=10, **params)


@pytest.mark.parametrize("alpha, delta", mix_coordinates())
def test_calculate_distance_mix_coordinate_system(alpha, delta, cf3_no_cache):
    cf3 = cf3_no_cache
    params = {alpha: 1, delta: 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        cf3.calculate_distance(velocity=10, **params)


def test_calculate_velocity_multiple_alpha(cf3_no_cache):
    cf3 = cf3_no_cache
    params = {"ra": 1, "dec": 1, "glon": 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        cf3.calculate_velocity(distance=10, **params)


def test_calculate_velocity_multiple_delta(cf3_no_cache):
    cf3 = cf3_no_cache
    params = {"ra": 1, "dec": 1, "glat": 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        cf3.calculate_velocity(distance=10, **params)


def test_calculate_distance_multiple_alpha(cf3_no_cache):
    cf3 = cf3_no_cache
    params = {"ra": 1, "dec": 1, "glon": 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        cf3.calculate_distance(velocity=10, **params)


def test_calculate_distance_multiple_delta(cf3_no_cache):
    cf3 = cf3_no_cache
    params = {"ra": 1, "dec": 1, "glat": 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        cf3.calculate_distance(velocity=10, **params)
