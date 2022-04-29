from abc import ABC
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import httpx

from bitbanker_sdk import utils
from bitbanker_sdk.dto import CreateInvoiceResponse
from bitbanker_sdk.dto import InvoiceData

BASE_URL: str = 'https://api.aws.bitbanker.org/latest/api'


class BitbankerError(Exception):
    pass


class BitbankerConnectionError(BitbankerError):
    pass


class BitbankerResponseError(BitbankerError):
    pass


class BaseClient(ABC):
    _CLIENT_CLASS: httpx.Client = httpx.Client
    _client: Optional[Union[httpx.Client, httpx.AsyncClient]] = None

    def __init__(self, api_key: str, timeout: Union[int, float] = 5) -> None:
        self.api_key: str = api_key
        self._headers: Dict[str, str] = {'X-API-KEY': self.api_key}
        if not self._client:
            self._client = self._CLIENT_CLASS(
                base_url=BASE_URL,
                timeout=httpx.Timeout(timeout),
                headers=self._headers,
            )

    def _get_sign(self, invoice_data: InvoiceData) -> str:
        message = f'{invoice_data.currency}{invoice_data.amount}{invoice_data.header}{invoice_data.description}'
        return utils.generate_sign(message, self.api_key)


class BitbankerClient(BaseClient):

    def create_invoice(self, invoice_data: InvoiceData):
        body: Dict[str, Any] = invoice_data.dict()
        body['sign'] = self._get_sign(invoice_data=invoice_data)
        body['amount'] = float(body['amount'])

        try:
            response = self._client.post('/v1/invoices', json=body)
        except Exception as exc:
            raise BitbankerConnectionError(exc)

        if response.status_code == httpx.codes.OK:
            return CreateInvoiceResponse.parse_obj(response.json())

        raise BitbankerResponseError(response.text)


class AsyncBitbankerClient(BaseClient):
    _CLIENT_CLASS: httpx.AsyncClient = httpx.AsyncClient

    async def create_invoice(self, invoice_data: InvoiceData) -> CreateInvoiceResponse:
        body: Dict[str, Any] = invoice_data.dict()
        body['sign'] = self._get_sign(invoice_data=invoice_data)
        body['amount'] = float(body['amount'])

        try:
            response = await self._client.post('/v1/invoices', json=body)
        except Exception as exc:
            raise BitbankerConnectionError(exc)

        if response.status_code == httpx.codes.OK:
            return CreateInvoiceResponse.parse_obj(response.json())

        raise BitbankerResponseError(response.text)
