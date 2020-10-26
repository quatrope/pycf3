.. pycf3 documentation master file, created by
   sphinx-quickstart on Sun Sep 22 19:13:13 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pycf3 - Cosmicflows-3 Distance-Velocity Calculator client for Python
====================================================================

.. image:: https://travis-ci.org/quatrope/pycf3.svg?branch=master
    :target: https://travis-ci.org/quatrope/pycf3

.. image:: https://readthedocs.org/projects/pycf3/badge/?version=latest
    :target: https://pycf3.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://badge.fury.io/py/pycf3
   :alt: Python 3.7+

.. image:: https://img.shields.io/badge/License-BSD3-blue.svg
   :target: https://tldrlegal.com/license/bsd-3-clause-license-(revised)
   :alt: License


Python client for Cosmicflows-3 Distance-Velocity Calculator at distances less
than 400 Mpc (http://edd.ifa.hawaii.edu/CF3calculator/)

Compute expectation distances or velocities based on smoothed velocity field
from the Wiener filter model of
`Graziani et al. 2019 <https://ui.adsabs.harvard.edu/abs/2019MNRAS.488.5438G/abstract>`_

More information: http://edd.ifa.hawaii.edu/CF3calculator/


Help & discussion mailing list
------------------------------


**You can contact me at:** jbc.develop@gmail.com


Code Repository & Issues
------------------------

https://github.com/quatrope/pycf3


License
-------

pycf3 is under
`The BSD 3 <https://raw.githubusercontent.com/quatrope/pycf3/master/LICENSE>`__

The BSD 3-clause license allows you almost unlimited freedom with the software so long as you include the BSD copyright and license notice in it (found in Fulltext).

Citation
--------

Please acknowledge pycf3 in any research report or publication that requires citation of any author's work.
Our suggested acknowledgment is:

    The authors acknowledge the pycf3 project that contributed to the research reported here. <https://pycf3.readthedocs.io/>


**ABOUT THE DATA**

All data exposed by pycf3 belongs to the project

    Cosmicflows-3 Distance-Velocity Calculato (http://edd.ifa.hawaii.edu/CF3calculator/)
    Copyright (C) Cosmicflows Team - The Extragalactic Distance Database (EDD)

Please cite:

    Kourkchi, E., Courtois, H. M., Graziani, R., Hoffman, Y., Pomarede, D.,
    Shaya, E. J., & Tully, R. B. (2020). Cosmicflows-3: Two Distance–Velocity
    Calculators. The Astronomical Journal, 159(2), 67.

BibText::

    @ARTICLE{2020AJ....159...67K,
        author = {{Kourkchi}, Ehsan and {Courtois}, H{\'e}l{\`e}ne M. and
         {Graziani}, Romain and {Hoffman}, Yehuda and {Pomar{\`e}de}, Daniel and
         {Shaya}, Edward J. and {Tully}, R. Brent},
        title = "{Cosmicflows-3: Two Distance-Velocity Calculators}",
        journal = {\aj},
        keywords = {590, 1146, 902, 1968, Astrophysics - Cosmology and
            Nongalactic Astrophysics, Astrophysics - Astrophysics of Galaxies,
            Astrophysics - Instrumentation and Methods for Astrophysics},
        year = 2020,
        month = feb,
        volume = {159},
        number = {2},
        eid = {67},
        pages = {67},
        doi = {10.3847/1538-3881/ab620e},
        archivePrefix = {arXiv},
        eprint = {1912.07214},
        primaryClass = {astro-ph.CO},
        adsurl = {https://ui.adsabs.harvard.edu/abs/2020AJ....159...67K},
        adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }


Authors
-------

Juan BC

jbc.develop@gmail.com

`IATE <http://iate.oac.uncor.edu/>`_ - `CIFASIS <https://www.cifasis-conicet.gov.ar/>`_

This project is part of the `QuatroPe <https://github.com/quatrope>`_ scientific
tools.


.. toctree::
    :maxdepth: 2
    :caption: Contents:

    install
    tutorial.ipynb
    api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
