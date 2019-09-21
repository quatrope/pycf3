#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Juan B Cabral
# License: BSD-3-Clause
#   Full Text: https://github.com/quatrope/cf3/blob/master/LICENSE


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

import numpy as np


# =============================================================================
# CONSTATS
# =============================================================================

URL = "http://edd.ifa.hawaii.edu/CF3calculator/"