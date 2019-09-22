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

from numpy import testing as npt

import pycf3


# =============================================================================
# EQUATORIAL TESTCASE
# =============================================================================

class TestCaseIntegrationEquatorial:

    def test_default(self):
        cf3 = pycf3.CF3()
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
        cf3 = pycf3.CF3()
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
        cf3 = pycf3.CF3()
        response = cf3.equatorial_search(velocity=10)

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)


# =============================================================================
# GALACTIC TEST CASE
# =============================================================================

class TestCaseIntegrationGalactic:

    def test_default(self):
        cf3 = pycf3.CF3()
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
        cf3 = pycf3.CF3()
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
        cf3 = pycf3.CF3()
        response = cf3.galactic_search(velocity=10)

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)


# =============================================================================
# SUPER-GALACTIC TEST CASE
# =============================================================================

class TestCaseIntegrationSuperGalactic:

    def test_default(self):
        cf3 = pycf3.CF3()
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
        cf3 = pycf3.CF3()
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
        cf3 = pycf3.CF3()
        response = cf3.supergalactic_search(velocity=10)

        assert response.Vls_Observed_ is None
        assert response.Vcls_Adjusted_ is None

        npt.assert_almost_equal(response.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(response.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(response.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(response.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(response.search_at_.sgb, -2.00000, decimal=4)
