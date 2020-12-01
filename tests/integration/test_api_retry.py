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

import requests

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
# RETRY
# =============================================================================


def test_integration_timeout(cf3_temp_cache, monkeypatch):
    monkeypatch.setattr(pycf3.CF3, "URL", "http://httpbin.org/delay/10")

    cf3 = cf3_temp_cache

    t0 = time.time()
    with pytest.raises(requests.ConnectionError), pytest.deprecated_call():
        cf3.equatorial_search(distance=10, timeout=2)
    total_time = time.time() - t0

    assert total_time > 2


def test_integration_http_status_500(cf3_temp_cache, monkeypatch):
    monkeypatch.setattr(pycf3.CF3, "URL", "http://httpbin.org/status/500")

    cf3 = cf3_temp_cache

    with pytest.raises(requests.exceptions.RetryError):
        with pytest.deprecated_call():
            cf3.equatorial_search(distance=10)
