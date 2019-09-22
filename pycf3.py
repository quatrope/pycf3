#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/pycf3/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Python client for Cosmicflows-3 Distance-Velocity Calculator at distances
less than 400 Mpc (http://edd.ifa.hawaii.edu/CF3calculator/)

Compute expectation distances or velocities based on smoothed velocity
field from the Wiener filter model of Graziani et al. 2019
(https://ui.adsabs.harvard.edu/abs/2019MNRAS.488.5438G/abstract).

More information: http://edd.ifa.hawaii.edu/CF3calculator/

"""


# =============================================================================
# IMPORTS
# =============================================================================

from enum import Enum

import attr

import requests


# =============================================================================
# CONSTANTS
# =============================================================================

class Coordinate(Enum):
    equatorial = "equatorial"
    galactic = "galactic"
    supergalactic = "supergalactic"


ALPHA = {
    Coordinate.equatorial: "ra",
    Coordinate.galactic: "glon",
    Coordinate.supergalactic: "sgl"
}


DELTA = {
    Coordinate.equatorial: "dec",
    Coordinate.galactic: "glat",
    Coordinate.supergalactic: "sgb"
}


URL = "http://edd.ifa.hawaii.edu/CF3calculator/getData.php"


# =============================================================================
# RESPONSE OBJECT
# =============================================================================

@attr.s(cmp=False, hash=False, repr=False)
class _Response:
    search = attr.ib()
    rresponse = attr.ib()


# =============================================================================
# CLIENT
# =============================================================================

@attr.s(cmp=False, hash=False)
class CF3:

    url = attr.ib(default=URL, repr=True)
    session = attr.ib(default=attr.Factory(requests.Session))

    def _search(self, coordinate, alpha, delta, cone,
                distance=None, velocity=None):

        # The validations
        if not isinstance(alpha, (int, float)):
            raise TypeError(f"{ALPHA[coordinate]} must be int or float")

        if not isinstance(delta, (int, float)):
            raise TypeError(f"{DELTA[coordinate]} must be int or float")
        elif not (-90 <= delta <= 90):
            raise ValueError(
                f"{DELTA[coordinate]} must be >= -90 and <= 90")

        if not isinstance(cone, (int, float)):
            raise TypeError(f"cone must be int or float")
        elif cone < 0:
            raise ValueError("Cone must be positive")

        if distance is not None and velocity is not None:
            raise ValueError(
                "You cant provide velocity and distance at the same time")
        elif distance is not None:
            if not isinstance(distance, (int, float)):
                raise TypeError("distance must be int, float or None")
                veldist = 0
        elif velocity is not None:
            if not isinstance(velocity, (int, float)):
                raise TypeError("distance must be int, float or None")
            veldist = 1
        else:
            veldist = -1

        payload = {
            "coordinate": coordinate,
            "alfa": alpha,
            "delta": delta,
            "cone": cone,
            "dist_t": "" if distance is None else distance,
            "vel_t": "" if velocity is None else velocity,
            "veldist": veldist}

        import ipdb; ipdb.set_trace()

    def equatorial_search(self, ra=187.78917, dec=13.33386, cone=10.0,
                          distance=None, velocity=None):
        response = self._search(
            Coordinate.equatorial, alpha=ra, delta=dec, cone=cone,
            distance=distance, velocity=velocity)
        return response

    def galactic_search(self, glon=282.96547, glat=75.41360, cone=10.0,
                        distance=None, velocity=None):
        response = self._search(
            Coordinate.galactic, alpha=glon, delta=glat, cone=cone,
            distance=distance, velocity=velocity)
        return response

    def supergalactic_search(self, sgl=102.0, sgb=-2.0, cone=10.0,
                             distance=None, velocity=None):
        response = self._search(
            Coordinate.supergalactic, alpha=sgl, delta=sgb, cone=cone,
            distance=distance, velocity=velocity)
        return response
