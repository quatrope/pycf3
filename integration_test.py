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
import pickle
from unittest import mock

import pytest

from numpy import testing as npt

import diskcache as dcache

import pycf3


# =============================================================================
# EQUATORIAL TESTCASE
# =============================================================================

class TestCaseIntegrationEquatorial:

    def teardown_method(self, method):
        s = random.randint(0, 1) + random.random()
        time.sleep(s)

    def test_default(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.equatorial_search()

        assert result.Vls_Observed_ is None
        assert result.Vcls_Adjusted_ is None

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    def test_distance_10(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.equatorial_search(distance=10)

        assert result.Vls_Observed_ == 730.
        assert result.Vcls_Adjusted_ == 691.

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    def test_velocity_10(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.equatorial_search(velocity=10)

        assert result.Vls_Observed_ is None
        assert result.Vcls_Adjusted_ is None

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


# =============================================================================
# GALACTIC TEST CASE
# =============================================================================

class TestCaseIntegrationGalactic:

    def teardown_method(self, method):
        s = random.randint(0, 1) + random.random()
        time.sleep(s)

    def test_default(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.galactic_search()

        assert result.Vls_Observed_ is None
        assert result.Vcls_Adjusted_ is None

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    def test_distance_10(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.galactic_search(distance=10)

        assert result.Vls_Observed_ == 730.
        assert result.Vcls_Adjusted_ == 691.

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    def test_velocity_10(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.galactic_search(velocity=10)

        assert result.Vls_Observed_ is None
        assert result.Vcls_Adjusted_ is None

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


# =============================================================================
# SUPER-GALACTIC TEST CASE
# =============================================================================

class TestCaseIntegrationSuperGalactic:

    def teardown_method(self, method):
        s = random.randint(0, 1) + random.random()
        time.sleep(s)

    def test_default(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.supergalactic_search()

        assert result.Vls_Observed_ is None
        assert result.Vcls_Adjusted_ is None

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    def test_distance_10(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.supergalactic_search(distance=10)

        assert result.Vls_Observed_ == 730.
        assert result.Vcls_Adjusted_ == 691.

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)

    def test_velocity_10(self):
        cf3 = pycf3.CF3(cache=pycf3.NoCache())
        result = cf3.supergalactic_search(velocity=10)

        assert result.Vls_Observed_ is None
        assert result.Vcls_Adjusted_ is None

        npt.assert_almost_equal(result.search_at_.ra, 187.78917, decimal=4)
        npt.assert_almost_equal(result.search_at_.dec, 13.33386, decimal=4)
        npt.assert_almost_equal(result.search_at_.glon, 282.96547, decimal=4)
        npt.assert_almost_equal(result.search_at_.glat, 75.41360, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgl, 102.00000, decimal=4)
        npt.assert_almost_equal(result.search_at_.sgb, -2.00000, decimal=4)


# =============================================================================
# CACHE TEST
# =============================================================================

class TestCaseIntegrationCache:

    @pytest.fixture
    def cache(self, tmp_path):
        cache = dcache.Cache(directory=tmp_path)
        yield cache
        cache.clear

    def test_cache(self, cache):
        with open("mock_data/tcEquatorial_default.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3(cache=cache)

        assert len(cache) == 0

        with mock.patch("requests.Session.post",
                        return_value=mresponse) as post:
            cf3.equatorial_search()
            cf3.equatorial_search()

        post.assert_called_once()
        assert len(cache) == 1

    def test_no_cache(self):
        with open("mock_data/tcEquatorial_default.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cache = pycf3.NoCache()
        cf3 = pycf3.CF3(cache=cache)

        assert len(cache) == 0
        with mock.patch("requests.Session.post",
                        return_value=mresponse) as post:
            cf3.equatorial_search()
            cf3.equatorial_search()

        assert post.call_count == 2
        assert len(cache) == 0

    def test_cache_expire(self, cache):
        with open("mock_data/tcEquatorial_default.pkl", "rb") as fp:
            mresponse = pickle.load(fp)

        cf3 = pycf3.CF3(cache=cache, cache_expire=2)

        assert len(cache) == 0
        with mock.patch("requests.Session.post",
                        return_value=mresponse) as post:
            cf3.equatorial_search()

            time.sleep(4)
            cache.expire()

            assert len(cache) == 0

            cf3.equatorial_search()

        assert post.call_count == 2
        assert len(cache) == 1
