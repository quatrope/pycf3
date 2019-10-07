pycf3 - Cosmicflows-3 Distance-Velocity Calculator client for Python
====================================================================

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

Python client for Cosmicflows-3 Distance-Velocity Calculator at distances less
than 400 Mpc (http://edd.ifa.hawaii.edu/CF3calculator/)

Compute expectation distances or velocities based on smoothed velocity field
from the Wiener filter model of
`Graziani et al. 2019 <https://ui.adsabs.harvard.edu/abs/2019MNRAS.488.5438G/abstract>`_.

More information: http://edd.ifa.hawaii.edu/CF3calculator/


Basic Install
-------------

Execute

.. code-block:: bash

    $ pip install pycf3


Development Install
--------------------

1.  Clone this repo and then inside the local
2.  Execute

    .. code-block:: bash

        $ pip install -e .

Tutorial
--------

https://pycf3.readthedocs.io


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
