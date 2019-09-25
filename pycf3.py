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


__all__ = ["CF3", "Result", "NoCache"]

__version__ = "2019.9.25"


# =============================================================================
# IMPORTS
# =============================================================================

from collections import namedtuple
from collections.abc import MutableMapping
from enum import Enum
import typing as t
import os

import attr

import diskcache as dcache

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


PYCF3_DATA = os.path.expanduser(os.path.join('~', 'pycf3_data'))


DEFAULT_CACHE_DIR = os.path.join(PYCF3_DATA, "_cache_")


# =============================================================================
# NO CACHE CLASS
# =============================================================================

class NoCache(MutableMapping):
    """Implements a no cache with the minimun methods to be useful with
    CF3 class"""

    def get(self, key, default=None, *args, **kwargs):
        """Always return the ``default``"""
        return default

    def set(self, key, value, *args, **kwargs):
        """This method do nothing. Always return True"""
        return True

    def __len__(self):
        return 0

    def __enter__(self):
        return self

    def __exit__(self, *exeption):
        pass

    def __delitem__(self, k):
        raise KeyError(k)

    def __getitem__(self, k):
        raise KeyError(k)

    def __iter__(self):
        return iter({})

    def __setitem__(self, k, v):
        pass


# =============================================================================
# RESPONSE OBJECT
# =============================================================================

SearchAt = namedtuple("SearchAt", ['ra', 'dec', 'glon', 'glat', 'sgl', 'sgb'])


@attr.s(cmp=False, hash=False, frozen=True)
class Result:
    r"""Parsed result of the *Cosmicflows-3 Distance-Velocity Calculator*-

    Parameters
    ----------

    coordinate : ``Coordinate``
        Coordinate system used to create this result.
    alpha : ``int`` or ``float``
        :math:`\alpha` value for the coordinate system.
    delta : ``int`` or ``float``
        :math:`\delta` value for the coordinate system.
    cone : ``int`` or ``float``
        Cone angle.
    distance : ``int``, ``float`` or ``None``
        Returns model velocity in km/s.
    velocity : ``int``, ``float`` or ``None``
        Returns model distance(s) in Mpc - potentially more than one value.

    Attributes
    ----------

    response_ : ``requests.Response``
        Original response object create by the *requests* library.
        More information: https://2.python-requests.org
    d_ : ``pyquery.PyQuery``
        Parsed *HTML* response inside a PyQuery object.
        More information: https://pythonhosted.org/pyquery/
    search_at_ : ``pycf3.SearhAt``
        :math:`\alpha` and :math:`\delta` in all the available coordinate
        systems.
    Vls_Observed_ : ``float`` or ``None``
        Observed velocity, :math:`V_{ls}`, vs. distance. `Vls_Observed_` is
        ``None`` if `distance` is ``None``
    Vcls_Adjusted_ : ``float`` or ``None``
        Cosmologically	adjusted velocity, :math:`V_{ls}^c`, vs. distance.
        The corrected velocity :math:`V_{ls}^c` is related to the observed
        velocity :math:`V_{ls}` by:

        .. math::

            V_{ls}^c = f(z)V_{ls}

        where

        .. math::

            f(z) = 1+1/2(1-q_0)z-1/6(2-q_0-3q_0^2)z^2

        .. math::

            q_0 = 1/2(\Omega_m-2\Omega_{\Lambda}) = -0.595

        when :math:`\Omega_m=0.27`, :math:`\Omega_{\Lambda}=0.73` and
        :math:`z=V_{ls}/c`.

        `Vcls_Adjusted_` is ``None`` if `distance` is ``None``.


    """

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
    (http://edd.ifa.hawaii.edu/CF3calculator/)

    Parameters
    ----------

    url : ``str`` (default: ``pycf3.URL``)
        The endpoint of the cosmic flow calculator.
    session : ``request.Session`` (default: ``None``)
        The session to use to send the requests. By default a session without
        any configuration is created. More info: https://2.python-requests.org
    cache : ``diskcache.Cache``, ``diskcache.Fanout``,
            ``pycf3.NoCache`` or ``None`` (default: ``None``)
        Any instance of ``diskcache.Cache``, ``diskcache.Fanout`` or
        ``None`` (Default). If it's ``None`` a ``diskcache.Cache`` istance
        is created with the parameter ``directory = pycf3.DEFAULT_CACHE_DIR``.
        More information: http://www.grantjenks.com/docs/diskcache
    cache_expire : ``float`` or None (default=``None``)
        Seconds until item expires (default ``None``, no expiry)
        More information: http://www.grantjenks.com/docs/diskcache

    """

    # =========================================================================
    # ATTRS SETUP
    # =========================================================================

    url: str = attr.ib(default=URL, repr=True)
    session: requests.Session = attr.ib(factory=requests.Session, repr=False)
    cache: t.Union[dcache.Cache, dcache.FanoutCache] = attr.ib()
    cache_expire: float = attr.ib(default=None, repr=False)

    @cache.default
    def _cache_default(self):
        return dcache.Cache(directory=DEFAULT_CACHE_DIR)

    # =========================================================================
    # INTERNAL
    # =========================================================================

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

        # start the cache orchestration
        base = (coordinate_system.value,)
        key = dcache.core.args_to_key(
            base=base, args=(self.url,), kwargs=payload, typed=False)

        with self.cache as cache:
            response = cache.get(key, default=dcache.core.ENOVAL, retry=True)
            if response == dcache.core.ENOVAL:
                response = self.session.post(self.url, payload)
                cache.set(
                    key, response, expire=self.cache_expire,
                    tag="@".join(key[:2]), retry=True)

        parsed_response = pq.PyQuery(response.text)

        result = Result(
            coordinate=coordinate_system, alpha=alpha, delta=delta, cone=cone,
            distance=distance, velocity=velocity,
            response_=response, d_=parsed_response)

        return result

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def equatorial_search(self, ra=187.78917, dec=13.33386, cone=10.0,
                          distance=None, velocity=None):
        """Search around the sky position expressed in equatorial coordinates
        (J2000 as 360° decimal) in degrees.

        Parameters
        ----------

        ra : ``int`` or ``float`` (default: ``187.78917``)
            Right ascension.
        dec : ``int`` or ``float`` (default: ``13.33386``)
            Declination. dec must be >= -90 and <= 90
        cone : ``int`` or ``float`` (default: ``10``)
            Points within this cone angle. cone must be >= 0.
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model velocity in km/s.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model distance(s) in Mpc - potentially more than one value.

        Returns
        -------

        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the *Cosmicflows-3 Distance-Velocity Calculator*.

        """
        response = self._search(
            CoordinateSystem.equatorial, alpha=ra, delta=dec, cone=cone,
            distance=distance, velocity=velocity)
        return response

    def galactic_search(self, glon=282.96547, glat=75.41360, cone=10.0,
                        distance=None, velocity=None):
        """Search around the sky position expressed in galactic coordinates
        (J2000 as 360° decimal) in degrees.

        Parameters
        ----------

        glon : ``int`` or ``float`` (default: ``282.96547``)
            Galactic longitude.
        glat: ``int`` or ``float`` (default: ``75.41360``)
            Galactic latitude. dec must be >= -90 and <= 90
        cone : ``int`` or ``float`` (default: ``10``)
            Points within this cone angle. cone must be >= 0.
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model velocity in km/s.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model distance(s) in Mpc - potentially more than one value.

        Returns
        -------

        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the *Cosmicflows-3 Distance-Velocity Calculator*.

        """
        response = self._search(
            CoordinateSystem.galactic, alpha=glon, delta=glat, cone=cone,
            distance=distance, velocity=velocity)
        return response

    def supergalactic_search(self, sgl=102.0, sgb=-2.0, cone=10.0,
                             distance=None, velocity=None):
        """Search around the sky position expressed in super-galactic
        coordinates (J2000 as 360° decimal) in degrees.

        Parameters
        ----------

        sgl : ``int`` or ``float`` (default: ``102``)
            Super-galactic longitude.
        sgb: ``int`` or ``float`` (default: ``-2``)
            Super-galactic latitude. dec must be >= -90 and <= 90
        cone : ``int`` or ``float`` (default: ``10``)
            Points within this cone angle. cone must be >= 0.
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model velocity in km/s.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model distance(s) in Mpc - potentially more than one value.

        Returns
        -------

        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the *Cosmicflows-3 Distance-Velocity Calculator*.

        """
        response = self._search(
            CoordinateSystem.supergalactic, alpha=sgl, delta=sgb, cone=cone,
            distance=distance, velocity=velocity)
        return response
