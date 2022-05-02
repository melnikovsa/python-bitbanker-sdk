from typing import Any


try:
    from unittest.mock import AsyncMock
except ImportError:
    from tests.mocks import AsyncMock  # type: ignore

import pytest

from bitbanker_sdk import AsyncBitbankerClient
from bitbanker_sdk import BitbankerConnectionError
from bitbanker_sdk import BitbankerResponseError
from bitbanker_sdk import CreateInvoiceResponse
from bitbanker_sdk import Currency
from bitbanker_sdk import InvoiceData
from tests.mocks import HttpResponseMock


@pytest.mark.asyncio
async def test_create_invoice_success(mocker: Any) -> None:
    mock = AsyncMock(
        return_value=HttpResponseMock(
            status_code=200,
            json={
                'result': 'success',
                'id': 'dfj5kpos6uacm',
                'link': 'https://app.dev.bitbanker.org/external/invoice/dfj5kpos6uacm',
                'addresses': {
                    'USDT': '0x36928500Bc1dCd7af6a2B4008875CC336b927D57',
                    'BTC': '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
                },
            },
        )
    )
    mocker.patch('httpx.AsyncClient.post', mock)

    client = AsyncBitbankerClient(api_key='key')
    data = InvoiceData(
        amount=1000,
        payment_currencies=[Currency.ETH, Currency.BTC],
        description='invoice number 1',
        header='invoice header',
    )
    response = await client.create_invoice(invoice_data=data)
    assert isinstance(response, CreateInvoiceResponse)
    assert response.result == 'success'
    assert response.id == 'dfj5kpos6uacm'
    assert response.link == 'https://app.dev.bitbanker.org/external/invoice/dfj5kpos6uacm'
    assert response.addresses['USDT'] == '0x36928500Bc1dCd7af6a2B4008875CC336b927D57'
    assert response.addresses['BTC'] == '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2'


@pytest.mark.asyncio
async def test_create_invoice_response_error(mocker: Any) -> None:
    mock = AsyncMock(return_value=HttpResponseMock(status_code=401, text='401: Unauthorized'))
    mocker.patch('httpx.AsyncClient.post', mock)

    client = AsyncBitbankerClient(api_key='key')
    data = InvoiceData(
        amount=1000,
        payment_currencies=[Currency.ETH, Currency.BTC],
        description='invoice number 1',
        header='invoice header',
    )

    with pytest.raises(BitbankerResponseError) as exc:
        await client.create_invoice(invoice_data=data)
        assert exc.value.args[1] == '401: Unauthorized'


@pytest.mark.asyncio
async def test_create_invoice_connection_error(mocker: Any) -> None:
    mock = AsyncMock(side_effect=RuntimeError())
    mocker.patch('httpx.AsyncClient.post', mock)

    client = AsyncBitbankerClient(api_key='key')
    data = InvoiceData(
        amount=1000,
        payment_currencies=[Currency.ETH, Currency.BTC],
        description='invoice number 1',
        header='invoice header',
    )

    with pytest.raises(BitbankerConnectionError):
        await client.create_invoice(invoice_data=data)
