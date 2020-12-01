#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, 2020 - Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/pycf3/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Configuration for unittests

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib

import diskcache as dcache

import joblib

import pycf3

import pytest

# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

MOCK_PATH = PATH / "mock_data"


# =============================================================================
# MARKERS
# =============================================================================


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.ALL)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture(scope="session")
def load_mresponse():
    def load(folder, fname):
        return joblib.load(MOCK_PATH / folder / fname)

    return load


@pytest.fixture
def no_cache():
    return pycf3.NoCache()


@pytest.fixture(scope="session")
def fakeclient_class():
    class Fake(pycf3.AbstractClient):
        CALCULATOR = "fake"
        URL = "nowhere://no.where"

    return Fake


@pytest.fixture
def tmp_cache(tmp_path):
    cache = dcache.Cache(directory=tmp_path)
    yield cache
    cache.clear()


@pytest.fixture
def fakeclient_no_cache(fakeclient_class, no_cache):
    return fakeclient_class(cache=no_cache)


@pytest.fixture
def fakeclient_temp_cache(fakeclient_class, tmp_cache):
    return fakeclient(cache=tmp_cache)


@pytest.fixture
def cf3_no_cache(no_cache):
    return pycf3.CF3(cache=no_cache)


@pytest.fixture
def cf3_temp_cache(tmp_cache):
    return pycf3.CF3(cache=tmp_cache)
