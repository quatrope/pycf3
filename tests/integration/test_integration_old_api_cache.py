#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/pycf3/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Integration Test for cache implementation.

Warning this code is SLOW!

"""


# =============================================================================
# IMPORTS
# =============================================================================

import random
import time

import pycf3

import pytest

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


# =============================================================================
# CACHE TEST
# =============================================================================


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
