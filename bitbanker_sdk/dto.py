from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from bitbanker_sdk.types_ import Currency
from bitbanker_sdk.types_ import Number
from bitbanker_sdk.types_ import connumber


class StrictBaseDTO(BaseModel):
    class Config:
        extra = 'forbid'


class InvoiceData(StrictBaseDTO):
    payment_currencies: List[Currency] = Field(
        description='Криптовалюты, в которых возможен прием платежей. Возможные значения: "BTC", "ETH"',
    )
    currency: Currency = Field(
        default=Currency.RUB,
        description='Валюта счета. Пока только рубли ("RUB").',
    )
    amount: connumber(ge=0.00000001) = Field(  # type: ignore
        description='Размер платежа в валюте, указанной в поле "currency".',
    )
    description: str = Field(
        description='Назначение платежа в произвольном формате.',
    )
    header: str = Field(
        description='Заголовок счета (название организации, которая выставила счет)',
    )
    is_convert_payments: bool = Field(
        default=False,
        description='Ковертировать поступившие средства в рубли или оставить в крипте',
    )
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description='Произвольные данные. Будут отправлены в запросе в webhook-е (если он настроен).',
    )

    class Config:
        schema_extra = {
            'example': {
                'payment_currencies': ['ETH', 'BTC'],
                'currency': 'RUB',
                'amount': 100,
                'description': 'Any text',
                'header': 'Any text',
                'sign': 'HUsdkjfh7s876w3bndsa98dyhsienjhHDJCH',
                'is_convert_payments': True,
                'data': {
                    'id': 1234,
                    'item': 'notebook',
                },
            }
        }
        dict_encoders = {Number: lambda v: float(v)}


class CreateInvoiceResponse(StrictBaseDTO):
    result: Literal['success']
    id: str
    link: str
    addresses: Dict[str, str]

    class Config:
        schema_extra = {
            'example': {
                'result': 'success',
                'id': 'dfj5kpos6uacm',
                'link': 'https://app.dev.bitbanker.org/external/invoice/dfj5kpos6uacm',
                'addresses': {
                    'USDT': '0x36928500Bc1dCd7af6a2B4008875CC336b927D57',
                    'BTC': '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
                },
            }
        }
