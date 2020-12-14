# pycf3 - Cosmicflows Galaxy Distance-Velocity Calculator client for Python

![image](https://raw.githubusercontent.com/quatrope/pycf3/master/res/logo.png)

----

[![QuatroPe](https://img.shields.io/badge/QuatroPe-Applications-1c5896)](https://quatrope.github.io/)
[![Travis-CI](https://travis-ci.com/quatrope/pycf3.svg?branch=master)](https://travis-ci.com/quatrope/pycf3)
[![ReadTheDocs.org](https://readthedocs.org/projects/pycf3/badge/?version=latest)](https://pycf3.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-BSD3-blue.svg)](https://www.tldrlegal.com/l/bsd3)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://badge.fury.io/py/pycf3)
[![PyPI](https://img.shields.io/pypi/v/pycf3)](https://pypi.org/project/pycf3/)


## Description

pycf3 is a Python client for the
[Cosmicflows-3 Distance-Velocity Calculator](http://edd.ifa.hawaii.edu/CF3calculator/),
and [NAM Distance-Velocity Calculator](http://edd.ifa.hawaii.edu/NAMcalculator/)


## Code Repository & Issues

https://github.com/quatrope/pycf3


## License

pycf3 is under [The BSD 3 License](https://www.tldrlegal.com/l/bsd3)

The BSD 3-clause license allows you almost unlimited freedom with the software
so long as you include the BSD copyright and license notice in it
(found in [Fulltext](https://raw.githubusercontent.com/quatrope/pycf3/master/LICENSE)).


## Basic Install


Execute

```console
$ pip install pycf3
```

## Development Install


Clone this repo and install with pip

```console
$ git clone https://github.com/quatrope/pycf3.git
$ cd pycf3
$ pip install -e .
```

## Quick Usage

```pycon
>>> import pycf3
>>> cf3 = pycf3.CF3()
>>> result = cf3.calculate_distance(velocity=9000, glon=283, glat=75)
>>> print(result.observed_velocity_)
9000.0
>>> result.observed_distance_
array([136.90134347])
```

For more information, read the [tutorial in the
documentation](https://pycf3.readthedocs.io).

## Citation

- If you use the results of this work in your research or other applications, 
please cite [Kourkchi et al. 2020, AJ, 159, 67](https://ui.adsabs.harvard.edu/abs/2020AJ....159...67K/abstract)
- Please acknowledge pycf3 in any research report or publication that
requires citation of any author\'s work. Our suggested acknowledgment
is:

> The authors acknowledge the pycf3 project that contributed to the
> research reported here. \<<https://pycf3.readthedocs.io/>\>

### ABOUT THE DATA

All data exposed by pycf3 belongs to the project

> Cosmicflows-3 Distance-Velocity Calculator
> (<http://edd.ifa.hawaii.edu/CF3calculator/>) Copyright (C) Cosmicflows
> Team - The Extragalactic Distance Database (EDD)

Please cite:

> Kourkchi, E., Courtois, H. M., Graziani, R., Hoffman, Y., Pomarede,
> D., Shaya, E. J., & Tully, R. B. (2020). Cosmicflows-3: Two
> Distance--Velocity Calculators. The Astronomical Journal, 159(2), 67.

#### BibText

```bib
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
```

## Authors


- Juan BC - [jbcabral@unc.edu.com](jbcabral@unc.edu.com)
- Bruno Sanchez
- Martin Beroiz
- Ehsan Kourkchi.


[IATE](http://iate.oac.uncor.edu/) -
[CIFASIS](https://www.cifasis-conicet.gov.ar/)

This project is part of the [QuatroPe](https://github.com/quatrope)
scientific tools.
