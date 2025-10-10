========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |github-actions| |coveralls| |codecov|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |commits-since|
.. |docs| image:: https://readthedocs.org/projects/django-siruta/badge/?style=flat
    :target: https://readthedocs.org/projects/django-siruta/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/ionelmc/django-siruta/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/ionelmc/django-siruta/actions

.. |coveralls| image:: https://coveralls.io/repos/github/ionelmc/django-siruta/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://coveralls.io/github/ionelmc/django-siruta?branch=main

.. |codecov| image:: https://codecov.io/gh/ionelmc/django-siruta/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/ionelmc/django-siruta

.. |version| image:: https://img.shields.io/pypi/v/django-siruta.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/django-siruta

.. |wheel| image:: https://img.shields.io/pypi/wheel/django-siruta.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/django-siruta

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/django-siruta.svg
    :alt: Supported versions
    :target: https://pypi.org/project/django-siruta

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/django-siruta.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/django-siruta

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/django-siruta/v0.1.1.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/django-siruta/compare/v0.1.1...main



.. end-badges

A bunch of form fields and utilities for Romanian counties and localities using SIRUTA codes.

* Free software: BSD 2-Clause License

Data:
    Localities: https://data.gov.ro/dataset/activity/siruta-2024
    Counties: https://data.gov.ro/dataset/activity/siruta

Form fields are designed to pass around integers (assuming you will have the most compact storage).

Form widgets use `selectize <https://selectize.dev/>`_.
JS/CSS not bundled or included in media - you are free to load those however you like.


Installation
============

::

    pip install django-siruta

You can also install the in-development version with::

    pip install https://github.com/ionelmc/django-siruta/archive/main.zip


Documentation
=============


https://django-siruta.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
