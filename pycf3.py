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

import pyquery as pq

import requests


# =============================================================================
# CONSTANTS
# =============================================================================

class CoordinateSystem(Enum):
    equatorial = "equatorial"
    galactic = "galactic"
    supergalactic = "supergalactic"


ALPHA = {
    CoordinateSystem.equatorial: "ra",
    CoordinateSystem.galactic: "glon",
    CoordinateSystem.supergalactic: "sgl"
}


DELTA = {
    CoordinateSystem.equatorial: "dec",
    CoordinateSystem.galactic: "glat",
    CoordinateSystem.supergalactic: "sgb"
}


URL = "http://edd.ifa.hawaii.edu/CF3calculator/getData.php"


# =============================================================================
# RESPONSE OBJECT
# =============================================================================

@attr.s(frozen=True)
class SearchAt:
    ra = attr.ib()
    dec = attr.ib()
    glon = attr.ib()
    glat = attr.ib()
    sgl = attr.ib()
    sgb = attr.ib()


@attr.s(cmp=False, hash=False, frozen=True)
class Response:
    coordinate = attr.ib()
    alpha = attr.ib()
    delta = attr.ib()
    cone = attr.ib()
    distance = attr.ib()
    velocity = attr.ib()

    response_ = attr.ib(repr=False)
    d_ = attr.ib(repr=False)

    search_at_ = attr.ib(init=False)
    Vls_Observed_ = attr.ib(repr=False, init=False)
    Vcls_Adjusted_ = attr.ib(repr=False, init=False)

    @search_at_.default
    def _search_at__default(self):
        coords_table = self.d_("table:last")

        eq_coords = coords_table.find("td:contains('RA:')").parent()
        ra, dec = (float(e.text) for e in eq_coords.find("td")[1::2])

        gal_coords = coords_table.find("td:contains('Glon:')").parent()
        glon, glat = (float(e.text) for e in gal_coords.find("td")[1::2])

        sg_coords = coords_table.find("td:contains('SGL:')").parent()
        sgl, sgb = (float(e.text) for e in sg_coords.find("td")[1::2])

        return SearchAt(ra=ra, dec=dec, glon=glon, glat=glat, sgl=sgl, sgb=sgb)

    @Vls_Observed_.default
    def _Vls_Observed__default(self):
        if self.distance is None:
            return None
        vlso_table = self.d_(
            "span:contains(' - Observed')").parents("table#calc")
        return float(vlso_table.find("td#calc")[1].text)

    @Vcls_Adjusted_.default
    def _Vcls_Adjusted__default(self):
        if self.distance is None:
            return None
        vclso_table = self.d_(
            "span:contains(' - Adjusted')").parents("table#calc")
        return float(vclso_table.find("td#calc")[1].text)


# =============================================================================
# CLIENT
# =============================================================================

@attr.s(cmp=False, hash=False, frozen=True)
class CF3:
    """Client to access the *Cosmicflows-3 Distance-Velocity Calculator*
    *at distances* (http://edd.ifa.hawaii.edu/CF3calculator/)

    Parameters
    ----------

    url : str (default: ``pycf3.URL``)
        The endpoint of the cosmic flow calculator.
    session : ``request.Session`` (default: ``None``)
        The session to use to send the requests. By default a session without
        any configuration is created. More info: https://2.python-requests.org

    """

    url: str = attr.ib(default=URL, repr=True)
    session: requests.Session = attr.ib(factory=requests.Session, repr=False)

    def _search(self, coordinate_system, alpha, delta, cone,
                distance=None, velocity=None):

        # The validations
        if coordinate_system not in CoordinateSystem:
            raise TypeError(
                "coordinate_system must be a member of "
                "pycf3.CoordinateSystem enum")

        if not isinstance(alpha, (int, float)):
            raise TypeError(f"{ALPHA[coordinate_system]} must be int or float")

        if not isinstance(delta, (int, float)):
            raise TypeError(f"{DELTA[coordinate_system]} must be int or float")
        elif not (-90 <= delta <= 90):
            raise ValueError(
                f"{DELTA[coordinate_system]} must be >= -90 and <= 90")

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
            "coordinate": coordinate_system.value,
            "alfa": alpha,
            "delta": delta,
            "cone": cone,
            "dist_t": "" if distance is None else distance,
            "vel_t": "" if velocity is None else velocity,
            "veldist": veldist}

        rresponse = self.session.post(self.url, payload)
        parsed_rresponse = pq.PyQuery(rresponse.text)

        response = Response(
            coordinate=coordinate_system, alpha=alpha, delta=delta, cone=cone,
            distance=distance, velocity=velocity,
            response_=rresponse, d_=parsed_rresponse)

        return response

    def equatorial_search(self, ra=187.78917, dec=13.33386, cone=10.0,
                          distance=None, velocity=None):
        response = self._search(
            CoordinateSystem.equatorial, alpha=ra, delta=dec, cone=cone,
            distance=distance, velocity=velocity)
        return response

    def galactic_search(self, glon=282.96547, glat=75.41360, cone=10.0,
                        distance=None, velocity=None):
        response = self._search(
            CoordinateSystem.galactic, alpha=glon, delta=glat, cone=cone,
            distance=distance, velocity=velocity)
        return response

    def supergalactic_search(self, sgl=102.0, sgb=-2.0, cone=10.0,
                             distance=None, velocity=None):
        response = self._search(
            CoordinateSystem.supergalactic, alpha=sgl, delta=sgb, cone=cone,
            distance=distance, velocity=velocity)
        return response
