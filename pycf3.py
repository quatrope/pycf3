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

All data exposed by pycf3 belongs to the project

Cosmicflows-3 Distance-Velocity Calculator
(http://edd.ifa.hawaii.edu/CF3calculator/)
Copyright (C) Cosmicflows Team
The Extragalactic Distance Database (EDD)

For citation check:
    https://github.com/quatrope/pycf3/blob/master/README.rst

"""


__all__ = ["CF3", "Result", "NoCache", "RetrySession"]

__version__ = "2020.11b"


# =============================================================================
# IMPORTS
# =============================================================================

import os
import typing as t
from collections import namedtuple
from collections.abc import MutableMapping
from enum import Enum

import attr

import diskcache as dcache

import numpy as np

import requests
from requests.packages.urllib3.util.retry import Retry

# =============================================================================
# CONSTANTS
# =============================================================================

class CoordinateSystem(Enum):
    equatorial = "equatorial"
    galactic = "galactic"
    supergalactic = "supergalactic"


class Parameter(Enum):
    distance = "distance"
    velocity = "velocity"


ALPHA = {
    CoordinateSystem.equatorial: "ra",
    CoordinateSystem.galactic: "glon",
    CoordinateSystem.supergalactic: "sgl",
}


DELTA = {
    CoordinateSystem.equatorial: "dec",
    CoordinateSystem.galactic: "glat",
    CoordinateSystem.supergalactic: "sgb",
}


PYCF3_DATA = os.path.expanduser(os.path.join("~", "pycf3_data"))


DEFAULT_CACHE_DIR = os.path.join(PYCF3_DATA, "_cache_")


# =============================================================================
# NO CACHE CLASS
# =============================================================================


class NoCache(MutableMapping):
    """Implements a no cache with the minimun methods to be used with
    CF3 class"""

    def get(self, key, default=None, *args, **kwargs):
        """Always return the ``default``"""
        return default

    def set(self, key, value, *args, **kwargs):
        """This method do nothing. Always return True"""
        return True

    def expire(self, now=None, retry=False):
        """Always return 0"""
        return 0

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
# SESSION OBJECT
# =============================================================================


class RetrySession(requests.Session):
    """Session with retry.

    Parameters
    ----------

    retries: ``int`` (default: ``3``)
        Total number of retries to allow.
        It's a good idea to set this to some sensibly-high value to
        account for unexpected edge cases and avoid infinite retry loops.
        Set to ``0`` to fail on the first retry.
    backoff_factor: ``float`` (default: ``0.3``)
        A backoff factor to apply between attempts after the second try (most
        errors are resolved immediately by a second try without a delay).
        urllib3 will sleep for:

            ``{backoff factor} * (2 ** ({number of total retries} - 1))``

        seconds. If the backoff_factor is ``0.1``, then ``sleep()`` will
        sleep for ``[0.0s, 0.2s, 0.4s, ...]`` between retries. It will never be
        longer than ``urllib3.Retry.BACKOFF_MAX``.

    status_forcelist: iterable (default: ``500, 502, 504``)

        A set of integer HTTP status codes that we should force a retry on. A
        retry is initiated if the request method is in method_whitelist and the
        response status code is in status_forcelist.

        By default, this is ``500, 502, 504``.


    """

    def __init__(
        self,
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        **session_options,
    ):
        super().__init__(**session_options)
        retries = retries or 0

        self.retry_ = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        self.adapter_ = requests.adapters.HTTPAdapter(max_retries=self.retry_)
        self.mount("http://", self.adapter_)
        self.mount("https://", self.adapter_)

        self.total_backoff_ = float(backoff_factor) * (2 ** (retries - 1))


# =============================================================================
# RESPONSE OBJECT
# =============================================================================

SearchAt = namedtuple("SearchAt", ["ra", "dec", "glon", "glat", "sgl", "sgb"])


@attr.s(eq=False, order=False, frozen=True)
class Result:
    r"""Parsed result -

    Parameters
    ----------

    calculator : ``str``
        The used calculator.
    url : ``str``
        The url of the calculator.
    coordinate : ``Coordinate``
        Coordinate system used to create this result.
    alpha : ``int`` or ``float``
        :math:`\alpha` value for the coordinate system.
    delta : ``int`` or ``float``
        :math:`\delta` value for the coordinate system.
    distance : ``int``, ``float`` or ``None``
        Returns model velocity in km/s.
    velocity : ``int``, ``float`` or ``None``
        Returns model distance(s) in Mpc - potentially more than one value.

    Attributes
    ----------

    response_ : ``requests.Response``
        Original response object create by the *requests* library.
        More information: https://2.python-requests.org

    json_: ``dict``
        The parsed data inside the response.


    """

    calculator = attr.ib()
    url = attr.ib(repr=False)

    coordinate = attr.ib()
    alpha = attr.ib()
    delta = attr.ib()
    distance = attr.ib()
    velocity = attr.ib()

    response_ = attr.ib(repr=False)

    observed_distance_ = attr.ib(init=False, repr=False)
    observed_velocity_ = attr.ib(init=False, repr=False)
    adjusted_distance_ = attr.ib(init=False, repr=False)
    adjusted_velocity_ = attr.ib(init=False, repr=False)

    search_at_ = attr.ib(init=False, repr=False)

    @property
    def json_(self):
        return self.response_.json()

    @observed_distance_.default
    def _observed_distance_default(self):
        return np.array(self.json_["observed"]["distance"])

    @observed_velocity_.default
    def _observed_velocity_default(self):
        return self.json_["observed"]["velocity"]

    @adjusted_distance_.default
    def _adjusted_distance_default(self):
        return np.array(self.json_["adjusted"]["distance"])

    @adjusted_velocity_.default
    def _adjusted_velocity_default(self):
        return self.json_["adjusted"]["velocity"]

    @search_at_.default
    def _search_at_default(self):
        data = self.json_
        return SearchAt(
            ra=data["RA"],
            dec=data["Dec"],
            glon=data["Glon"],
            glat=data["Glat"],
            sgl=data["SGL"],
            sgb=data["SGB"],
        )


# =============================================================================
# CLIENT
# =============================================================================


@attr.s(eq=False, order=False, frozen=True)
class CF3:
    """Client to access the *Cosmicflows-3 Distance-Velocity Calculator*
    (http://edd.ifa.hawaii.edu/CF3calculator/)

    Parameters
    ----------

    session : ``pycf3.Session`` (default: ``None``)
        The session to use to send the requests. By default a
        ``pyc3.RetrySession`` with 3 retry is created. More info:
        https://2.python-requests.org,
        https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html.
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

    CALCULATOR = "CF3"
    URL = "http://edd.ifa.hawaii.edu/CF3calculator/api.php"

    # =========================================================================
    # ATTRS SETUP
    # =========================================================================

    session: requests.Session = attr.ib(factory=RetrySession, repr=False)
    cache: t.Union[dcache.Cache, dcache.FanoutCache] = attr.ib()
    cache_expire: float = attr.ib(default=None, repr=False)

    @cache.default
    def _cache_default(self):
        return dcache.Cache(directory=DEFAULT_CACHE_DIR)

    # =========================================================================
    # INTERNAL
    # =========================================================================

    def _search(
        self,
        coordinate_system,
        alpha,
        delta,
        distance=None,
        velocity=None,
        **get_kwargs,
    ):

        # The validations
        if coordinate_system not in CoordinateSystem:
            raise TypeError(
                "coordinate_system must be a member of "
                "pycf3.CoordinateSystem enum"
            )

        if not isinstance(alpha, (int, float)):
            raise TypeError(f"{ALPHA[coordinate_system]} must be int or float")

        if not isinstance(delta, (int, float)):
            raise TypeError(f"{DELTA[coordinate_system]} must be int or float")
        elif not (-90 <= delta <= 90):
            raise ValueError(
                f"{DELTA[coordinate_system]} must be >= -90 and <= 90"
            )

        if (distance, velocity) == (None, None):
            raise ValueError(
                "You must provide the distance or the velocity value"
            )
        elif distance is not None and velocity is not None:
            raise ValueError(
                "You cant provide velocity and distance at the same time"
            )
        elif distance is not None:
            if not isinstance(distance, (int, float)):
                raise TypeError("distance must be int, float or None")
            parameter, value = Parameter.distance, distance
        elif velocity is not None:
            if not isinstance(velocity, (int, float)):
                raise TypeError("distance must be int, float or None")
            parameter, value = Parameter.velocity, velocity

        payload = {
            "coordinate": [float(alpha), float(delta)],
            "system": coordinate_system.value,
            "parameter": parameter.value,
            "value": float(value),
        }

        # start the cache orchestration
        base = (
            self.CALCULATOR,
            coordinate_system.value,
        )
        key = dcache.core.args_to_key(
            base=base, args=(self.URL,), kwargs=payload, typed=False
        )

        with self.cache as cache:
            cache.expire()
            response = cache.get(key, default=dcache.core.ENOVAL, retry=True)
            if response == dcache.core.ENOVAL:
                response = self.session.get(
                    self.URL, json=payload, **get_kwargs
                )
                response.raise_for_status()
                cache.set(
                    key,
                    response,
                    expire=self.cache_expire,
                    tag="@".join(key[:2]),
                    retry=True,
                )

        result = Result(
            calculator=self.CALCULATOR,
            url=self.URL,
            coordinate=coordinate_system,
            alpha=alpha,
            delta=delta,
            distance=distance,
            velocity=velocity,
            response_=response,
        )

        return result

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def equatorial_search(
        self,
        ra=187.78917,
        dec=13.33386,
        distance=None,
        velocity=None,
        **get_kwargs,
    ):
        """Search around the sky position expressed in equatorial coordinates
        (J2000 as 360° decimal) in degrees.

        Parameters
        ----------

        ra : ``int`` or ``float`` (default: ``187.78917``)
            Right ascension.
        dec : ``int`` or ``float`` (default: ``13.33386``)
            Declination. dec must be >= -90 and <= 90
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model velocity in km/s.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model distance(s) in Mpc - potentially more than one value.
        get_kwargs:
            Optional arguments that ``request.get`` takes.

        Returns
        -------

        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the *Cosmicflows-3 Distance-Velocity Calculator*.

        """
        response = self._search(
            CoordinateSystem.equatorial,
            alpha=ra,
            delta=dec,
            distance=distance,
            velocity=velocity,
            **get_kwargs,
        )
        return response

    def galactic_search(
        self,
        glon=282.96547,
        glat=75.41360,
        distance=None,
        velocity=None,
        **get_kwargs,
    ):
        """Search around the sky position expressed in galactic coordinates
        (J2000 as 360° decimal) in degrees.

        Parameters
        ----------

        glon : ``int`` or ``float`` (default: ``282.96547``)
            Galactic longitude.
        glat: ``int`` or ``float`` (default: ``75.41360``)
            Galactic latitude. dec must be >= -90 and <= 90
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model velocity in km/s.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model distance(s) in Mpc - potentially more than one value.
        get_kwargs:
            Optional arguments that ``request.get`` takes.

        Returns
        -------

        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the *Cosmicflows-3 Distance-Velocity Calculator*.

        """
        response = self._search(
            CoordinateSystem.galactic,
            alpha=glon,
            delta=glat,
            distance=distance,
            velocity=velocity,
            **get_kwargs,
        )
        return response

    def supergalactic_search(
        self,
        sgl=102.0,
        sgb=-2.0,
        distance=None,
        velocity=None,
        **get_kwargs,
    ):
        """Search around the sky position expressed in super-galactic
        coordinates (J2000 as 360° decimal) in degrees.

        Parameters
        ----------

        sgl : ``int`` or ``float`` (default: ``102``)
            Super-galactic longitude.
        sgb: ``int`` or ``float`` (default: ``-2``)
            Super-galactic latitude. dec must be >= -90 and <= 90
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model velocity in km/s.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Returns model distance(s) in Mpc - potentially more than one value.
        get_kwargs:
            Optional arguments that ``request.get`` takes.

        Returns
        -------

        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the *Cosmicflows-3 Distance-Velocity Calculator*.

        """
        response = self._search(
            CoordinateSystem.supergalactic,
            alpha=sgl,
            delta=sgb,
            distance=distance,
            velocity=velocity,
            **get_kwargs,
        )
        return response
