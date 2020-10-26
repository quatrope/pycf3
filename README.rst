pycf3 - Cosmicflows-3 Galaxy Distance-Velocity Calculator client for Python
===========================================================================

.. image:: https://travis-ci.org/quatrope/pycf3.svg?branch=master
    :target: https://travis-ci.org/quatrope/pycf3
    :alt: Build Status

.. image:: https://readthedocs.org/projects/pycf3/badge/?version=latest
    :target: https://pycf3.readthedocs.io/en/latest/?badge=latest
    :alt: ReadTheDocs.org

.. image:: https://img.shields.io/badge/License-BSD3-blue.svg
   :target: https://tldrlegal.com/license/bsd-3-clause-license-(revised)
   :alt: License

.. image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://badge.fury.io/py/pycf3
   :alt: Python 3.7+


Description
-----------

pycf3 is a Python client for the Cosmicflows-3 Distance-Velocity Calculator
best suited for distances closer than 400 Mpc (http://edd.ifa.hawaii.edu/CF3calculator/)

Galaxy velocities deviate from Hubble-Lemaitre expansion.
Deviations can be considerable, as evidenced by the motion of the Local Group
of 631 km s−1 with respect to the rest frame of the cosmic microwave background.

The Cosmicflows-3 Distance-Velocity Calculator delivers a better approximation
between observed velocities and physical distances than provided by the simple
assumption of uniform cosmic expansion.

It computes expectation distances or velocities based on a velocity field
responding to the full complexity of structure on scales 1 − 200 Mpc, smoothed
from the Wiener filter model of
`Graziani et al. 2019 <https://ui.adsabs.harvard.edu/abs/2019MNRAS.488.5438G/abstract>`_.

For more information, please visit the `Extragalactic Distance Database website <http://edd.ifa.hawaii.edu/CF3calculator>`_
and read the relevant publication
`Cosmicflows-3: Two Distance-Velocity Calculators <https://ui.adsabs.harvard.edu/abs/2020AJ....159...67K/abstract>`_.


Basic Install
-------------

Execute

.. code-block:: bash

    $ pip install pycf3


Development Install
--------------------

Clone this repo and install with pip

    .. code-block:: bash

        $ git clone https://github.com/quatrope/pycf3.git
        $ cd pycf3
        $ pip install -e .

Quick Usage
-----------

    .. code-block:: python

        import pycf3
        cf3 = pycf3.CF3()
        cf3.supergalactic_search(sgl=102.0, sgb=-2.0, cone=10.0, distance=None, velocity=None)
        result = cf3.supergalactic_search(distance=10)
        print(result.Vls_Observed_)
        print(result.Vls_Observed_)

For more information, read the `tutorial in the documentation <https://pycf3.readthedocs.io>`_.


Citation
--------

Please acknowledge pycf3 in any research report or publication that requires citation of any author's work.
Our suggested acknowledgment is:

    The authors acknowledge the pycf3 project that contributed to the research reported here. <https://pycf3.readthedocs.io/>


**ABOUT THE DATA**

All data exposed by pycf3 belongs to the project

    Cosmicflows-3 Distance-Velocity Calculator (http://edd.ifa.hawaii.edu/CF3calculator/)
    Copyright (C) Cosmicflows Team - The Extragalactic Distance Database (EDD)

Please cite:

    Shaya, E. J., Tully, R. B., Hoffman, Y., & Pomarède, D. (2017). Action dynamics
    of the local supercluster. arXiv preprint arXiv:1710.08935.

BibText::

    @article{shaya2017action,
        title={Action dynamics of the local supercluster},
        author={Shaya, Edward J and Tully, R Brent and Hoffman, Yehuda and Pomar{\`e}de, Daniel},
        journal={arXiv preprint arXiv:1710.08935},
        year={2017}
    }


Authors
-------

Juan BC

jbc.develop@gmail.com

`IATE <http://iate.oac.uncor.edu/>`_ - `CIFASIS <https://www.cifasis-conicet.gov.ar/>`_

This project is part of the `QuatroPe <https://github.com/quatrope>`_ scientific
tools.
