# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import pathlib


# this path is pointing to project/docs/source
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
PROJECT_PATH = CURRENT_PATH.parent.parent

sys.path.insert(0, str(PROJECT_PATH))


# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

import pycf3


# -- Project information -----------------------------------------------------

project = 'pycf3'
copyright = '2019, QuatroPe'
author = 'QuatroPe'

# The full version, including alpha/beta/rc tags
release = pycf3.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'IPython.sphinxext.ipython_console_highlighting']

exclude_patterns = ['_build', 'source/.ipynb_checkpoints/*']

numpydoc_class_members_toctree = False

nbsphinx_execute = 'never'  # access the server is slow


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

master_doc = 'index'

# =============================================================================
# PREPROCESS RST
# =============================================================================

import m2r2

with open(PROJECT_PATH / "README.md") as fp:
    md = fp.read()


index = f"""

{m2r2.convert(md)}

Contents:
---------

.. toctree::
    :maxdepth: 3

    tutorial.ipynb
    api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

"""

with open(CURRENT_PATH / "index.rst", "w") as fp:
    fp.write(index)
