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

import diskcache as dcache

from numpy import testing as npt

import pycf3

import pytest

import requests

# =============================================================================
# MARKERS
# =============================================================================

pytestmark = pytest.mark.integration


# =============================================================================
# SLEEP BASE
# =============================================================================


def teardown_function(function):
    s = random.random()
    time.sleep(s)


# # =============================================================================
# # CACHE TEST
# # =============================================================================


def test_integration_cache(tmp_cache):
    cache = tmp_cache
    cf3 = pycf3.CF3(cache=cache)

    assert len(cache) == 0

    cf3.equatorial_search(velocity=10)
    cf3.equatorial_search(velocity=10)

    assert len(cache) == 1


def test_integration_no_cache(no_cache):
    cache = no_cache

    cf3 = pycf3.CF3(cache=cache)

    assert len(cache) == 0

    cf3.equatorial_search(velocity=10)
    cf3.equatorial_search(velocity=10)

    assert len(cache) == 0


def test_integration_cache_expire(tmp_cache):
    cache = tmp_cache

    cf3 = pycf3.CF3(cache=cache, cache_expire=2)

    assert len(cache) == 0

    cf3.equatorial_search(distance=10)

    assert len(cache) == 1

    time.sleep(3)

    cf3.equatorial_search(distance=10)

    assert len(cache) == 1


# # =============================================================================
# # RETRY
# # =============================================================================


# class Clock:
#     def __enter__(self):
#         self._t0 = time.time()
#         return self

#     def __exit__(self, *err):
#         self.total_time = time.time() - self._t0
#         del self._t0


# class TestCaseIntegrationRetry(SleepBase):
#     @pytest.fixture
#     def cache(self, tmp_path):
#         cache = pycf3.NoCache()
#         yield cache
#         cache.clear()

#     def test_timeout(self, cache):
#         cf3 = pycf3.CF3(cache=cache, url="http://httpbin.org/delay/10")
#         with pytest.raises(requests.ReadTimeout), Clock() as clock:
#             cf3.equatorial_search(timeout=2)

#         assert clock.total_time > 2 and clock.total_time < 3

#     def test_500(self, cache):
#         cf3 = pycf3.CF3(cache=cache, url="http://httpbin.org/status/500")
#         with pytest.raises(requests.HTTPError):
#             cf3.equatorial_search()

#     def test_502(self, cache):
#         cf3 = pycf3.CF3(cache=cache, url="http://httpbin.org/status/502")
#         with pytest.raises(requests.HTTPError):
#             cf3.equatorial_search()

#     def test_504(self, cache):
#         cf3 = pycf3.CF3(cache=cache, url="http://httpbin.org/status/504")
#         with pytest.raises(requests.HTTPError):
#             cf3.equatorial_search()
