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


def test_integration_timeout(
    fakeclient_class, fakeclient_temp_cache, monkeypatch
):
    monkeypatch.setattr(fakeclient_class, "URL", "http://httpbin.org/delay/5")

    client = fakeclient_temp_cache

    t0 = time.time()
    with pytest.raises(requests.ConnectionError):
        client.calculate_velocity(
            ra=187.78917, dec=13.33386, distance=10, timeout=2
        )
    total_time = time.time() - t0

    assert total_time > 2


def test_integration_timeout(
    fakeclient_class, fakeclient_temp_cache, monkeypatch
):
    monkeypatch.setattr(
        fakeclient_class, "URL", "http://httpbin.org/status/500"
    )

    client = fakeclient_temp_cache

    with pytest.raises(requests.exceptions.RetryError):
        client.calculate_velocity(ra=187.78917, dec=13.33386, distance=10)
