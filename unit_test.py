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

from numpy import testing as npt

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

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)

    def test_distance_10(self):
        with open("mock_data/tcEquatorial_distance_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.equatorial_search(distance=10)

        assert response.Vls_Observed_ == 730.
        assert response.Vcls_Adjusted_ == 691.

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)

    def test_velocity_10(self):
        with open("mock_data/tcEquatorial_velocity_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.equatorial_search(velocity=10)

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)

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

    def test_default(self):
        with open("mock_data/tcGalactic_default.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.galactic_search()

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)

    def test_distance_10(self):
        with open("mock_data/tcGalactic_distance_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.galactic_search(distance=10)

        assert response.Vls_Observed_ == 730.
        assert response.Vcls_Adjusted_ == 691.

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)

    def test_velocity_10(self):
        with open("mock_data/tcGalactic_velocity_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.galactic_search(velocity=10)

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)

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


# =============================================================================
# SUPER-GALACTIC TEST CASE
# =============================================================================

class TestCaseSuperGalactic:

    def test_default(self):
        with open("mock_data/tcSuperGalactic_default.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.supergalactic_search()

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)


    def test_distance_10(self):
        with open("mock_data/tcSuperGalactic_distance_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.supergalactic_search(distance=10)

        assert response.Vls_Observed_ == 730.
        assert response.Vcls_Adjusted_ == 691.

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)

    def test_velocity_10(self):
        with open("mock_data/tcSuperGalactic_velocity_10.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3()
        with mock.patch("requests.Session.post", return_value=mresponse):
            response = cf3.supergalactic_search(velocity=10)

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)

    def test_sgl_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.supergalactic_search(sgl="foo")

    def test_sgb_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.supergalactic_search(sgb="foo")

    def test_sgb_lt_m90(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.supergalactic_search(sgb=-91)

    def test_sgb_gt_90(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.supergalactic_search(sgb=91)

    def test_cone_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.supergalactic_search(cone="foo")

    def test_cone_lt_0(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.supergalactic_search(cone=-91)

    def test_distance_velocity_together(self):
        cf3 = pycf3.CF3()
        with pytest.raises(ValueError):
            cf3.supergalactic_search(distance=10, velocity=10)

    def test_distance_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.supergalactic_search(distance="foo")

    def test_velocity_not_number(self):
        cf3 = pycf3.CF3()
        with pytest.raises(TypeError):
            cf3.supergalactic_search(distance="foo")
