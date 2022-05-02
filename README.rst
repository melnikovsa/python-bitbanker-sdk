bitbanker-sdk
-----------------

.. image:: https://img.shields.io/pypi/v/bitbanker-sdk.svg
    :target: https://pypi.python.org/pypi/bitbanker-sdk

.. image:: https://img.shields.io/pypi/pyversions/bitbanker-sdk.svg
    :target: https://pypi.python.org/pypi/bitbanker-sdk

.. image:: https://codecov.io/gh/melnikovsa/python-bitbanker-sdk/branch/main/graph/badge.svg
    :target: https://app.codecov.io/gh/melnikovsa/python-bitbanker-sdk

.. image:: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/tests.yml

.. image:: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/pypi.yml/badge.svg
    :target: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/pypi.yml

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
With sync python application::

    from bitbanker_sdk import BitbankerClient
    from bitbanker_sdk import InvoiceData
    from bitbanker_sdk import Currency

    client = BitbankerClient(api_key="<your bitbanker api key>")
    invoice_data = InvoiceData(
            amount=1000,
            payment_currencies=[Currency.ETH, Currency.BTC],
            description='invoice description',
            header='invoice header'
        )

    response = client.create_invoice(invoice_data=invoice_data)
    print(response.link)

With async python application::

    from bitbanker_sdk import AsyncBitbankerClient
    from bitbanker_sdk import InvoiceData
    from bitbanker_sdk import Currency

    client = AsyncBitbankerClient(api_key="<your bitbanker api key>")
    invoice_data = InvoiceData(
            amount=1000,
            payment_currencies=[Currency.ETH, Currency.BTC],
            description='invoice description',
            header='invoice header'
        )

    response = await client.create_invoice(invoice_data=invoice_data)
    print(response.link)
