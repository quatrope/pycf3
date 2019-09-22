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

import pytest

import pycf3


# =============================================================================
# EQUATORIAL TESTCASE
# =============================================================================

class TestCaseEquatorial:

    def test_default(self):
        with open("mock_data/tcEquatorial_default.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.equatorial_search()

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

    def test_distance_10(self):
        with open("mock_data/tcEquatorial_distance_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.equatorial_search(distance=10)

        assert response.Vls_Observed_ == 730.
        assert response.Vcls_Adjusted_ == 691.

    def test_velocity_10(self):
        with open("mock_data/tcEquatorial_velocity_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.equatorial_search(velocity=10)

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

    def test_ra_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.equatorial_search(ra="foo")

    def test_dec_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.equatorial_search(dec="foo")

    def test_dec_lt_m90(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.equatorial_search(dec=-91)

    def test_dec_gt_90(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.equatorial_search(dec=91)

    def test_cone_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.equatorial_search(cone="foo")

    def test_cone_lt_0(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.equatorial_search(cone=-91)

    def test_distance_velocity_together(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.equatorial_search(distance=10, velocity=10)

    def test_distance_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.equatorial_search(distance="foo")

    def test_velocity_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.equatorial_search(distance="foo")


# =============================================================================
# GALACTIC TEST CASE
# =============================================================================

class TestCaseGalactic:

    def __persist(self):
        coord = "Galactic"
        conf = {
            f"tc{coord}_default.pkl": {},
            f"tc{coord}_distance_10.pkl": {"distance": 10},
            f"tc{coord}_velocity_10.pkl": {"velocity": 10},
        }
        for fname, params in conf.items():
            cf3 = pycf3.CF3()
            response = cf3.galactic_search(**params)
            with open(f"mock_data/{fname}", "wb") as fp:
                pickle.dump(response.response_, fp)


    def test_default(self):
        with open("mock_data/tcGalactic_default.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.galactic_search()

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

    def test_distance_10(self):
        with open("mock_data/tcGalactic_distance_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.galactic_search(distance=10)

        assert response.Vls_Observed_ == 730.
        assert response.Vcls_Adjusted_ == 691.

    def test_velocity_10(self):
        with open("mock_data/tcGalactic_velocity_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.galactic_search(velocity=10)

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

    def test_glon_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.galactic_search(glon="foo")

    def test_glat_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.galactic_search(glat="foo")

    def test_glat_lt_m90(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.galactic_search(glat=-91)

    def test_glat_gt_90(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.galactic_search(glat=91)

    def test_cone_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.galactic_search(cone="foo")

    def test_cone_lt_0(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.galactic_search(cone=-91)

    def test_distance_velocity_together(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.galactic_search(distance=10, velocity=10)

    def test_distance_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.galactic_search(distance="foo")

    def test_velocity_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.galactic_search(distance="foo")