#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/pycf3/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================


"""Test for Python common functionalities in all CosmicFlow

"""


# =============================================================================
# IMPORTS
# =============================================================================

import itertools as it

import pycf3

import pytest


# =============================================================================
# INTERNAL TESTS
# =============================================================================


def test_client_repr(fakeclient_no_cache):
    result = repr(fakeclient_no_cache)
    expected = "Fake(calculator='fake', cache_dir='', cache_expire=None)"
    assert result == expected


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
def test_calculate_distance_velocity_eq_0(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_distance(velocity=0, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_distance_velocity_lt_0(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_distance(velocity=-1, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_distance_velocity_not_number(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(TypeError):
        client.calculate_distance(velocity="invalid", **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": "invalid"},
        {"glon": 282.96547, "glat": "invalid"},
        {"sgl": 102.0, "sgb": "invalid"},
    ],
)
def test_calculate_distance_delta_not_number(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(TypeError):
        client.calculate_distance(velocity="invalid", **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": "invalid", "dec": 13.33386},
        {"glon": "invalid", "glat": 75.4136},
        {"sgl": "invalid", "sgb": -2.0},
    ],
)
def test_calculate_distance_alpha_not_number(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(TypeError):
        client.calculate_distance(velocity=10, **params)


# =============================================================================
# calculate_distance BAD COORDINATES
# =============================================================================


def test_calculate_distance_no_coordinates(fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_distance(velocity=10)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 1, "dec": 91},
        {"glon": 1, "glat": 91},
        {"sgl": 1, "sgb": 91},
    ],
)
def test_calculate_distance_delta_gt_90(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_distance(velocity=10, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 1, "dec": -91},
        {"glon": 1, "glat": -91},
        {"sgl": 1, "sgb": -91},
    ],
)
def test_calculate_distance_delta_lt_m90(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_distance(velocity=10, **params)


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
def test_calculate_velocity_distance_eq_0(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_velocity(distance=0, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_velocity_distance_lt_0(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_velocity(distance=-1, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": 13.33386},
        {"glon": 282.96547, "glat": 75.4136},
        {"sgl": 102.0, "sgb": -2.0},
    ],
)
def test_calculate_velocity_distance_not_number(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(TypeError):
        client.calculate_velocity(distance="invalid", **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": "invalid", "dec": 13.33386},
        {"glon": "invalid", "glat": 75.4136},
        {"sgl": "invalid", "sgb": -2.0},
    ],
)
def test_calculate_velocity_alpha_not_number(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(TypeError):
        client.calculate_velocity(distance=10, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 187.78917, "dec": "invalid"},
        {"glon": 282.96547, "glat": "invalid"},
        {"sgl": 102.0, "sgb": "invalid"},
    ],
)
def test_calculate_velocity_delta_not_number(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(TypeError):
        client.calculate_velocity(distance=10, **params)


# =============================================================================
# calculate_velocity BAD COORDINATES
# =============================================================================


def test_calculate_velocity_no_coordinates(fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_velocity(distance=10)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 1, "dec": 91},
        {"glon": 1, "glat": 91},
        {"sgl": 1, "sgb": 91},
    ],
)
def test_calculate_velocity_delta_gt_90(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_velocity(distance=10, **params)


@pytest.mark.parametrize(
    "params",
    [
        {"ra": 1, "dec": -91},
        {"glon": 1, "glat": -91},
        {"sgl": 1, "sgb": -91},
    ],
)
def test_calculate_velocity_delta_lt_m90(params, fakeclient_no_cache):
    client = fakeclient_no_cache
    with pytest.raises(ValueError):
        client.calculate_velocity(distance=10, **params)


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
def test_calculate_velocity_mix_coordinate_system(
    alpha, delta, fakeclient_no_cache
):
    client = fakeclient_no_cache
    params = {alpha: 1, delta: 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        client.calculate_velocity(distance=10, **params)


@pytest.mark.parametrize("alpha, delta", mix_coordinates())
def test_calculate_distance_mix_coordinate_system(
    alpha, delta, fakeclient_no_cache
):
    client = fakeclient_no_cache
    params = {alpha: 1, delta: 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        client.calculate_distance(velocity=10, **params)


def test_calculate_velocity_multiple_alpha(fakeclient_no_cache):
    client = fakeclient_no_cache
    params = {"ra": 1, "dec": 1, "glon": 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        client.calculate_velocity(distance=10, **params)


def test_calculate_velocity_multiple_delta(fakeclient_no_cache):
    client = fakeclient_no_cache
    params = {"ra": 1, "dec": 1, "glat": 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        client.calculate_velocity(distance=10, **params)


def test_calculate_distance_multiple_alpha(fakeclient_no_cache):
    client = fakeclient_no_cache
    params = {"ra": 1, "dec": 1, "glon": 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        client.calculate_distance(velocity=10, **params)


def test_calculate_distance_multiple_delta(fakeclient_no_cache):
    client = fakeclient_no_cache
    params = {"ra": 1, "dec": 1, "glat": 1}
    with pytest.raises(pycf3.MixedCoordinateSystemError):
        client.calculate_distance(velocity=10, **params)
