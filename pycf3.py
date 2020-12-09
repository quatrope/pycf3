#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/pycf3/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Python client for several cosmic distance calculators.

Calculators:

- Cosmicflows-3 Distance-Velocity Calculator at distances
- Numerical Action Methods model

More information: http://edd.ifa.hawaii.edu/CF3calculator/

For citation check:
    https://github.com/quatrope/pycf3/blob/master/README.rst

"""


__all__ = [
    "AbstractClient",
    "NAM",
    "CF3",
    "Result",
    "NoCache",
    "RetrySession",
    "CFDeprecationWarning",
    "MixedCoordinateSystemError",
]

__version__ = "2020.12"


# =============================================================================
# IMPORTS
# =============================================================================

import itertools as it
import json
import os
import typing as t
from collections import namedtuple
from collections.abc import MutableMapping
from enum import Enum

import attr

from custom_inherit import DocInheritMeta

from deprecated import deprecated

import diskcache as dcache

import numpy as np

import requests
from requests.packages.urllib3.util.retry import Retry

import tabulate


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

ALPHA_TO_COORDINATE = {v: k for k, v in ALPHA.items()}

DELTA = {
    CoordinateSystem.equatorial: "dec",
    CoordinateSystem.galactic: "glat",
    CoordinateSystem.supergalactic: "sgb",
}

DELTA_TO_COORDINATE = {v: k for k, v in DELTA.items()}

ALPHA_DELTA_TO_COORDINATE = dict(
    it.chain(ALPHA_TO_COORDINATE.items(), DELTA_TO_COORDINATE.items())
)

PYCF3_DATA = os.path.expanduser(os.path.join("~", "pycf3_data"))


DEFAULT_CACHE_DIR = os.path.join(PYCF3_DATA, "_cache_")

RESULT_HTML_TEMPLATE = """
<div class="result-container" id="result-{{ id_result }}">
    <div class="result-css">
        <style>
            .observed {
                color: #dc3545! important;
            }

            .adjusted {
                color: #28a745!important;
            }


            tablr.result-table, div.result-raw {
                width: 100%;
            }

            table.result-table tr{
                 pointer-events: none;
                 background-color: inherit !important;
            }

            .result-container code{
                color: #e83e8c;
                background-color: inherit !important;
            }

            .result-container .hidden {
                display: none;
            }

            div.result-raw {
                background-color: #333 !important;
            }
        </style>
    </div>
    <div class="result-container container-fluid">
        <table class="result-table">
            <thead>
                <th colspan=3>
                    Result - <small><code>{{ call_result }}</code></small>
                </th>
            </thead>
            <tbody>
                <tr>
                    <th rowspan=2 class="observed">Observed</th>
                    <td>Distance (Mpc)</td>
                    <td>
                        {{ result.observed_distance_ }}
                    </td>
                </tr>
                <tr>
                    <td>Velocity (Km/s)</td>
                    <td>
                        {{ result.observed_velocity_ }}
                    </td>
                </tr>
                {% if result.adjusted_distance_ or result.adjusted_velocity_ %}
                <tr>
                    <th rowspan=2 class="adjusted">Adjusted</th>
                    <td>Distance (Mpc)</td>
                    <td>
                        {{ result.adjusted_distance_ }}
                    </td>
                </tr>
                <tr>
                    <td>Velocity (Km/s)</td>
                    <td>
                        {{ result.adjusted_velocity_ }}
                    </td>
                </tr>
                {% endif %}
            </tbody>
        </table>
        <div class="">
            <a onclick="return showRaw{{ id_result }}();" href="#">
                Show/Hide Raw
            </a>
            <div class="result-raw">
                <code id="result-code-{{ id_result }}" class="hidden">
{{ json_result }}
                </code>
            </div>
        </div>
    </div>
    <div class="result-js">
        <script>
            function showRaw{{ id_result }}(){
                var showed = document.getElementById(
                    "result-code-{{ id_result }}"
                ).classList.toggle("hidden");
                return false;
            }
        </script>
    </div>
</div>
"""


# =============================================================================
# EXCEPTIONS
# =============================================================================


class MixedCoordinateSystemError(ValueError):
    """Raised when the parameters are from different coordinates systems."""


class CFDeprecationWarning(DeprecationWarning):
    """Custom class to inform that some functionality is in desuse."""


# =============================================================================
# RETRY SESSION IMPLEMENTATION
# =============================================================================


class RetrySession(requests.Session):
    r"""Session with retry.

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
        """Create a new instance."""
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
# NO CACHE CLASS
# =============================================================================


class NoCache(MutableMapping):
    """Implements a minimalist no-cache for disk-cache."""

    def get(self, key, default=None, *args, **kwargs):
        """Return the ``default``."""
        return default

    def set(self, key, value, *args, **kwargs):
        """Return True."""
        return True

    def expire(self, now=None, retry=False):
        """Return 0."""
        return 0

    def __len__(self):
        """Return 0."""
        return 0

    def __enter__(self):
        """Enter the runtime context related to this object.

        The with statement will bind this method’s return value to the
        target(s) specified in the as clause of the statement, if any.

        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object.

        The parameters describe the exception that caused the context to be
        exited. If the context was exited without an exception, all three
        arguments will be None.

        """
        pass

    def __delitem__(self, k):
        """Raise KeyError."""
        raise KeyError(k)

    def __getitem__(self, k):
        """Raise KeyError."""
        raise KeyError(k)

    def __iter__(self):
        """Return an empty iterator."""
        return iter({})

    def __setitem__(self, k, v):
        """Do nothing."""
        pass


# =============================================================================
# RESPONSE OBJECT
# =============================================================================

CalculatedAt = namedtuple(
    "CalculatedAt", ["ra", "dec", "glon", "glat", "sgl", "sgb"]
)


@attr.s(eq=False, order=False, frozen=True, repr=False)
class Result:
    r"""Parsed result.

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
        Distance used to calculate the velocity in Mpc.
    velocity : ``int``, ``float`` or ``None``
        Velocity used to calculate the distance in Km/s.

    Attributes
    ----------
    response_ : ``requests.Response``
        Original response object create by the *requests* library.
        More information: https://2.python-requests.org
    observed_distance_: ``numpy.ndarray``
        Observed distances.
    observed_velocity_: ``float``
        Observed velocity
    adjusted_distance_: ``numpy.ndarray``
        Cosmologically adjusted distances.
    adjusted_velocity_: ``float``
        Cosmologically adjusted velocity, :math:`V^c_{ls}`.
    calculated_at_: ``pycf3.CalculatedAt``
        Coordinates in all the three supported systems.

    """

    calculator = attr.ib()
    url = attr.ib(repr=False)

    coordinate = attr.ib()
    calculated_by = attr.ib()
    alpha = attr.ib()
    delta = attr.ib()
    distance = attr.ib()
    velocity = attr.ib()

    response_ = attr.ib(repr=False)

    observed_distance_ = attr.ib(init=False, repr=False)
    observed_velocity_ = attr.ib(init=False, repr=False)
    adjusted_distance_ = attr.ib(init=False, repr=False)
    adjusted_velocity_ = attr.ib(init=False, repr=False)

    calculated_at_ = attr.ib(init=False, repr=False)

    # =========================================================================
    # INTERNAL
    # =========================================================================

    def _get_call_result(self):
        alpha_name, delta_name = ALPHA[self.coordinate], DELTA[self.coordinate]

        value = (
            self.distance
            if self.calculated_by == Parameter.distance
            else self.velocity
        )

        call_result = (
            f"{self.calculator}("
            f"{self.calculated_by.value}={value}, "
            f"{alpha_name}={self.alpha}, "
            f"{delta_name}={self.delta})"
        )

        return call_result

    def __repr__(self):
        """x.__repr__() <==> repr(x)."""
        # header
        call_result = self._get_call_result()
        header = f"Result - {call_result}"

        # body
        table = []
        table.append(
            [
                "Observed\n\n",
                "Distance (Mpc)\nVelocity (Km/s)",
                f"{self.observed_distance_}\n{self.observed_velocity_}",
            ]
        )
        if self.adjusted_distance_ or self.adjusted_velocity_:
            table.append(
                [
                    "Adjusted\n\n",
                    "Distance (Mpc)\nVelocity (Km/s)",
                    f"{self.adjusted_distance_}\n{self.adjusted_velocity_}",
                ]
            )
        body = tabulate.tabulate(table, headers="", tablefmt="grid")

        # merge and return
        return f"{header}\n{body}"

    def _repr_html_(self):
        """Create an HTML representation of the result.

        Mostly used inside jupyter environment.

        """
        import jinja2  # noqa

        call_result = self._get_call_result()

        id_result = str(id(self) + np.random.random()).replace(".", "rr")

        params = {
            "result": self,
            "id_result": id_result,
            "call_result": call_result,
            "json_result": json.dumps(self.json_, indent=2),
        }
        return jinja2.Template(RESULT_HTML_TEMPLATE).render(**params)

    @property
    def json_(self):
        """Proxy to ``response_.json()``."""
        return self.response_.json()

    @observed_distance_.default
    def _observed_distance_default(self):
        if "observed" in self.json_:
            return np.array(self.json_["observed"]["distance"])
        return np.array(self.json_["distance"])

    @observed_velocity_.default
    def _observed_velocity_default(self):
        if "observed" in self.json_:
            return self.json_["observed"]["velocity"]
        return self.json_["velocity"]

    @adjusted_distance_.default
    def _adjusted_distance_default(self):
        try:
            return np.array(self.json_["adjusted"]["distance"])
        except KeyError:
            return None

    @adjusted_velocity_.default
    def _adjusted_velocity_default(self):
        try:
            return self.json_["adjusted"]["velocity"]
        except KeyError:
            return None

    @calculated_at_.default
    def _calculated_at_default(self):
        data = self.json_
        return CalculatedAt(
            ra=data["RA"],
            dec=data["Dec"],
            glon=data["Glon"],
            glat=data["Glat"],
            sgl=data["SGL"],
            sgb=data["SGB"],
        )

    # =========================================================================
    # DEPRECATED API
    # =========================================================================

    @property
    @deprecated(
        category=CFDeprecationWarning,
        action="once",
        reason="Use `calculated_by` instead",
        version="2020.12",
    )
    def search_by(self):
        """Proxy to ``response.calculated_by``.

        .. deprecated:: 2020.12
            "Use `calculated_by` instead"

        """
        return self.calculated_by

    @property
    @deprecated(
        category=CFDeprecationWarning,
        action="once",
        reason="Use `calculated_at_` instead",
        version="2020.12",
    )
    def search_at_(self):
        """Proxy to ``response.calculated_at_``.

        .. deprecated:: 2020.12
            "Use `calculated_at` instead"

        """
        return self.calculated_at_


# =============================================================================
# ABSTRACT CLIENT
# =============================================================================


@attr.s(eq=False, order=False, frozen=True, repr=False)
class AbstractClient(metaclass=DocInheritMeta(style="numpy")):
    """Abstract base class for all clients.

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

    session: requests.Session = attr.ib(factory=RetrySession, repr=False)
    cache: t.Union[dcache.Cache, dcache.FanoutCache] = attr.ib()
    cache_expire: float = attr.ib(default=None, repr=False)

    @cache.default
    def _cache_default(self):
        return dcache.Cache(directory=DEFAULT_CACHE_DIR)

    def _determine_coordinate_system(self, ra, dec, glon, glat, sgl, sgb):

        # first we put all the parameters in a single dictionary
        params = {
            "ra": ra,
            "dec": dec,
            "glon": glon,
            "glat": glat,
            "sgl": sgl,
            "sgb": sgb,
        }

        # next we remove all keys with the default value `None`
        params = {k: v for k, v in params.items() if v is not None}

        # if we have 0 values no coordinate was given
        if len(params) == 0:
            raise ValueError(
                "No coordinate was provided. "
                "Please provide (ra, dec)', '(glon, glat)' or '(sgl, sgb)'."
            )

        # if we only have one we need to check wich one and inform about
        # the mising companinon
        if len(params) == 1:
            pname = list(params.keys())[0]
            coordinate_system, companion_dict = (
                (ALPHA_TO_COORDINATE[pname], DELTA)
                if pname in ALPHA_TO_COORDINATE
                else (DELTA_TO_COORDINATE[pname], ALPHA)
            )
            companion = companion_dict[coordinate_system]
            raise ValueError(f"No {companion} provided")

        # if we have more than two parameter we have mixed coordinate system
        if len(params) > 2:
            raise MixedCoordinateSystemError(", ".join(params))

        # now we need to detemine the coordinate system
        coordinate_system_candidates = {
            ALPHA_DELTA_TO_COORDINATE[p] for p in params.keys()
        }

        # if we have more than 1 candidate we mix coordinates again
        if len(coordinate_system_candidates) > 1:
            raise MixedCoordinateSystemError(", ".join(params))

        # we have one coordinate system and we need to dermermine which
        # is alpha and wich is delta
        coordinate_system = coordinate_system_candidates.pop()
        alpha_coordinate_name = ALPHA[coordinate_system]
        delta_coordinate_name = DELTA[coordinate_system]

        alpha = params[alpha_coordinate_name]
        delta = params[delta_coordinate_name]

        return coordinate_system, alpha, delta

    def _search(
        self,
        coordinate_system,
        alpha,
        delta,
        distance,
        velocity,
        **get_kwargs,
    ):

        # The validations
        if coordinate_system not in CoordinateSystem:
            raise TypeError(
                "coordinate_system must be a member of "
                "pycf3.core.CoordinateSystem enum"
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

        if distance is not None:
            if not isinstance(distance, (int, float)):
                raise TypeError("'distance' must be int or float")
            elif not (0 < distance <= self.MAX_DISTANCE):
                raise ValueError(
                    f"'distance' must be > 0 and <= {self.MAX_DISTANCE}"
                )
            parameter, value = Parameter.distance, distance

        elif velocity is not None:
            if not isinstance(velocity, (int, float)):
                raise TypeError("'velocity' must be int or float")
            elif not (0 < velocity <= self.MAX_VELOCITY):
                raise ValueError(
                    f"'velocity' must be > 0 and <= {self.MAX_VELOCITY}"
                )

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
            calculated_by=parameter,
            alpha=alpha,
            delta=delta,
            distance=distance,
            velocity=velocity,
            response_=response,
        )

        return result

    # =========================================================================
    # INTERNALS
    # =========================================================================

    def __repr__(self):
        """x.__repr__() <==> repr(x)."""
        cls = type(self).__name__
        calculator = f"calculator='{self.CALCULATOR}'"
        cachedir = f"cache_dir='{getattr(self.cache, 'directory', '')}'"
        expire = f"cache_expire={self.cache_expire}"
        return f"{cls}({calculator}, {cachedir}, {expire})"

    # =========================================================================
    # API
    # =========================================================================

    def calculate_distance(
        self,
        velocity,
        *,
        ra=None,
        dec=None,
        glon=None,
        glat=None,
        sgl=None,
        sgb=None,
        **get_kwargs,
    ):
        """Calculate a distance based on the given velocity and location.

        The mandatory parameters are ``velocity`` and a position
        expressed in two components depending on the chosen coordinate system:

         - ``ra`` and ``dec`` for an equatorial system.
         - ``glon`` and ``glat`` for a galactic system.
         - ``sgl`` and ``sgb`` for a supergalactic system.

        Coordinates cannot be mixed between systems, and must be expressed in
        J2000 as 360° decimal.

        The returned distance(s) are expressed in Mpc, and potentially can
        be more than one value.

        Parameters
        ----------
        velocity : ``int`` or ``float``
            Model velocity in km/s.
        ra : ``int`` or ``float`` (optional)
            Right ascension. If you provide ``ra`` you need to provide also
            ``dec``.
        dec : ``int`` or ``float`` (optional)
            Declination. ``dec`` must be >= -90 and <= 90. If you provide
            ``dec`` you need to provide also ``ra``.
        glon : ``int`` or ``float`` (optional)
            Galactic longitude. If you provide ``glon`` you need to provide
            also ``glat``.
        glat: ``int`` or ``float`` (optional)
            Galactic latitude. ``glat`` must be >= -90 and <= 90. If you
            provide ``glat`` you need to provide also ``glon``.
        sgl : ``int`` or ``float`` (optional)
            Super-galactic longitude. If you provide ``sgl`` you need to
            provide also ``sgb``.
        sgb: ``int`` or ``float`` (optional)
            Super-galactic latitude. ``sgb`` must be >= -90 and <= 90.
            If you  provide ``sgb`` you need to provide also ``sgl``.
        get_kwargs:
            Optional arguments that ``request.get`` takes.

        Returns
        -------
        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the remote calculator.

        """
        coordinate_system, alpha, delta = self._determine_coordinate_system(
            ra=ra, dec=dec, glon=glon, glat=glat, sgl=sgl, sgb=sgb
        )
        response = self._search(
            coordinate_system=coordinate_system,
            alpha=alpha,
            delta=delta,
            distance=None,
            velocity=velocity,
            **get_kwargs,
        )
        return response

    def calculate_velocity(
        self,
        distance,
        *,
        ra=None,
        dec=None,
        glon=None,
        glat=None,
        sgl=None,
        sgb=None,
        **get_kwargs,
    ):
        """Calculate a velocity based on the given distance and location.

        The mandatory parameters are ``distance`` and a position
        expressed in two components depending on the chosen coordinate system:

         - ``ra`` and ``dec`` for an equatorial system.
         - ``glon`` and ``glat`` for a galactic system.
         - ``sgl`` and ``sgb`` for a supergalactic system.

        Coordinates cannot be mixed between systems, and must be expressed in
        J2000 as 360° decimal.

        The returned velocity are expressed in Km/s.

        Parameters
        ----------
        distance : ``int`` or ``float``
            Distance(s) in Mpc.
        ra : ``int`` or ``float`` (optional)
            Right ascension. If you provide ``ra`` you need to provide also
            ``dec``.
        dec : ``int`` or ``float`` (optional)
            Declination. ``dec`` must be >= -90 and <= 90. If you provide
            ``dec`` you need to provide also ``ra``.
        glon : ``int`` or ``float`` (optional)
            Galactic longitude. If you provide ``glon`` you need to provide
            also ``glat``.
        glat: ``int`` or ``float`` (optional)
            Galactic latitude. ``glat`` must be >= -90 and <= 90. If you
            provide ``glat`` you need to provide also ``glon``.
        sgl : ``int`` or ``float`` (optional)
            Super-galactic longitude. If you provide ``sgl`` you need to
            provide also ``sgb``.
        sgb: ``int`` or ``float`` (optional)
            Super-galactic latitude. ``sgb`` must be >= -90 and <= 90.
            If you  provide ``sgb`` you need to provide also ``sgl``.
        get_kwargs:
            Optional arguments that ``request.get`` takes.

        Returns
        -------
        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the remote calculator.

        """
        coordinate_system, alpha, delta = self._determine_coordinate_system(
            ra=ra, dec=dec, glon=glon, glat=glat, sgl=sgl, sgb=sgb
        )
        response = self._search(
            coordinate_system=coordinate_system,
            alpha=alpha,
            delta=delta,
            distance=distance,
            velocity=None,
            **get_kwargs,
        )
        return response

    # =========================================================================
    # OLD API
    # =========================================================================

    @deprecated(
        category=CFDeprecationWarning,
        action="once",
        reason="Use `calculate_velocity` or `calculate_distance` instead",
        version="2020.12",
    )
    def equatorial_search(
        self,
        ra=187.78917,
        dec=13.33386,
        distance=None,
        velocity=None,
        **get_kwargs,
    ):
        """Search by equatorial coordinates.

        The coordinates are expressed in J2000 as 360° decimal.

        .. deprecated:: 2020.12
            "Use `calculate_velocity` or `calculate_distance` instead"

        Parameters
        ----------
        ra : ``int`` or ``float`` (default: ``187.78917``)
            Right ascension.
        dec : ``int`` or ``float`` (default: ``13.33386``)
            Declination. dec must be >= -90 and <= 90
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Distance(s) in Mpc.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Velocity in km/s. The returned distance potentially can be more
            than ine value.
        get_kwargs:
            Optional arguments that ``request.get`` takes.

        Returns
        -------
        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the remote calculator.

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

    @deprecated(
        category=CFDeprecationWarning,
        action="once",
        reason="Use `calculate_velocity` or `calculate_distance` instead",
        version="2020.12",
    )
    def galactic_search(
        self,
        glon=282.96547,
        glat=75.41360,
        distance=None,
        velocity=None,
        **get_kwargs,
    ):
        """Search by galactic coordinates.

        The coordinates are expressed in J2000 as 360° decimal.

        .. deprecated:: 2020.12
            "Use `calculate_velocity` or `calculate_distance` instead"

        Parameters
        ----------
        glon : ``int`` or ``float`` (default: ``282.96547``)
            Galactic longitude.
        glat: ``int`` or ``float`` (default: ``75.41360``)
            Galactic latitude. dec must be >= -90 and <= 90
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Distance(s) in Mpc.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Velocity in km/s. The returned distance potentially can be more
            than ine value.
        get_kwargs:
            Optional arguments that ``request.get`` takes.

        Returns
        -------
        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the remote calculator.

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

    @deprecated(
        category=CFDeprecationWarning,
        action="once",
        reason="Use `calculate_velocity` or `calculate_distance` instead",
        version="2020.12",
    )
    def supergalactic_search(
        self,
        sgl=102.0,
        sgb=-2.0,
        distance=None,
        velocity=None,
        **get_kwargs,
    ):
        """Search super-galactic coordinates.

        The coordinates are expressed in J2000 as 360° decimal.

        .. deprecated:: 2020.12
            "Use `calculate_velocity` or `calculate_distance` instead"

        Parameters
        ----------
        sgl : ``int`` or ``float`` (default: ``102``)
            Super-galactic longitude.
        sgb: ``int`` or ``float`` (default: ``-2``)
            Super-galactic latitude. dec must be >= -90 and <= 90
        distance : ``int``, ``float`` or ``None`` (default: ``None``)
            Distance(s) in Mpc.
        velocity : ``int``, ``float`` or ``None`` (default: ``None``)
            Velocity in km/s. The returned distance potentially can be more
            than ine value.
        get_kwargs:
            Optional arguments that ``request.get`` takes.

        Returns
        -------
        pycf3.Result :
            Result object that automatically parses the entire model
            returned by the remote calculator.

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


# =============================================================================
# NAM CLIENT
# =============================================================================


class NAM(AbstractClient):
    """Client for the *NAM Distance-Velocity Calculator* [1]_.

    Compute expectation distances or velocities based on smoothed velocity
    field from the Numerical Action Methods model of Shaya et al. 2017. [2]_.

    More information: http://edd.ifa.hawaii.edu/NAMcalculator.

    References
    ----------
    .. [1] Kourkchi, E., Courtois, H. M., Graziani, R., Hoffman, Y.,
       Pomarede, D., Shaya, E. J., & Tully, R. B. (2020).
       Cosmicflows-3: Two Distance-Velocity Calculators.
       The Astronomical Journal, 159(2), 67.

    .. [2] Shaya, E. J., Tully, R. B., Hoffman, Y., & Pomarède, D. (2017).
       Action dynamics of the local supercluster.
       The Astrophysical Journal, 850(2), 207.

    """

    CALCULATOR = "NAM"
    URL = "http://edd.ifa.hawaii.edu/NAMcalculator/api.php"

    #: Maximum distance to adjust the velocity.
    MAX_DISTANCE = 38

    #: Maximum velocity to adjust the distance.
    MAX_VELOCITY = 2400


# =============================================================================
# CF3 CLIENT
# =============================================================================


class CF3(AbstractClient):
    """Client for the *Cosmicflows-3 Distance-Velocity Calculator* [3]_.

    It computes expectation distances or velocities based on smoothed
    velocity field from the Wiener filter model of Graziani et al. 2019 [4]_.

    More information: http://edd.ifa.hawaii.edu/CF3calculator/ .

    References
    ----------
    .. [3] Kourkchi, E., Courtois, H. M., Graziani, R., Hoffman, Y.,
       Pomarede, D., Shaya, E. J., & Tully, R. B. (2020).
       Cosmicflows-3: Two Distance-Velocity Calculators.
       The Astronomical Journal, 159(2), 67.

    .. [4] Graziani, R., Courtois, H. M., Lavaux, G., Hoffman, Y.,
       Tully, R. B., Copin, Y., & Pomarède, D. (2019).
       The peculiar velocity field up to z∼ 0.05 by forward-modelling
       Cosmicflows-3 data. Monthly Notices of the Royal Astronomical Society,
       488(4), 5438-5451.

    """

    CALCULATOR = "CF3"
    URL = "http://edd.ifa.hawaii.edu/CF3calculator/api.php"

    #: Maximum distance to adjust the velocity.
    MAX_DISTANCE = 200

    #: Maximum velocity to adjust the distance.
    MAX_VELOCITY = 15_000
