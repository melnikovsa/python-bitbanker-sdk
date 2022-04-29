bitbanker-sdk
-----------------

.. image:: https://img.shields.io/pypi/v/bitbanker-sdk.svg
    :target: https://pypi.python.org/pypi/bitbanker-sdk

.. image:: https://img.shields.io/pypi/pyversions/bitbanker-sdk.svg
    :target: https://pypi.python.org/pypi/bitbanker-sdk

.. image:: https://github.com/GenyaSol/aiocircuitbreaker/actions/workflows/run-test.yml/badge.svg
    :target: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/tests.yml

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black


This is an sync/async Python `Bitbanker`__ API client.

.. _Bitbanker: https://bitbanker.org/

__ Bitbanker_


Installation
------------

The project is available on PyPI. Simply run::

    $ pip install bitbanker-sdk


Usage
-----
::

    from aiocircuitbreaker import circuit

    @circuit
    async def external_call():
        ...

