import decimal
import enum
from decimal import ROUND_DOWN
from typing import Any
from typing import Dict
from typing import Type
from typing import Union

import pydantic
from pydantic.types import ConstrainedNumberMeta
from pydantic.types import OptionalInt
from pydantic.types import OptionalIntFloatDecimal
from pydantic.validators import decimal_validator
from pydantic.validators import number_multiple_validator
from pydantic.validators import number_size_validator


DEFAULT_PRECISION = 12
DEFAULT_QUANTIZE_EXP = decimal.Decimal(str(10**-DEFAULT_PRECISION))


class Context(pydantic.BaseModel):
    exchange_id: int
    market_id: int


class PrecisionType(enum.Enum):
    AMOUNT = 'amount'
    PRICE = 'price'
    COST = 'cost'


class Currency(str, enum.Enum):
    RUB = 'RUB'
    BTC = 'BTC'
    ETH = 'ETH'


class PydanticMixin:
    """
    Базовая поддержка pydantic
    """

    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return cls(v)
        except Exception:
            raise ValueError(f'Invalid type of {v}: {type(v)}')


class Number(PydanticMixin, decimal.Decimal):
    def __new__(cls, value: Union[int, float, str, decimal.Decimal] = '0'):
        if isinstance(value, (int, float, decimal.Decimal)):
            value = str(value)
        self = decimal.Decimal.__new__(Number, value)
        self = self.quantize(DEFAULT_QUANTIZE_EXP, rounding=ROUND_DOWN)
        self = decimal.Decimal.__new__(Number, self)
        return self

    def __add__(self, other, *args, **kwargs):
        return self.__run_operator('__add__', other, *args, **kwargs)

    def __sub__(self, other, *args, **kwargs):
        return self.__run_operator('__sub__', other, *args, **kwargs)

    def __mul__(self, other, *args, **kwargs):
        return self.__run_operator('__mul__', other, *args, **kwargs)

    def __truediv__(self, other, *args, **kwargs):
        return self.__run_operator('__truediv__', other, *args, **kwargs)

    def __gt__(self, other, *args, **kwargs):
        return self.__run_comparator('__gt__', other, *args, **kwargs)

    def __lt__(self, other, *args, **kwargs):
        return self.__run_comparator('__lt__', other, *args, **kwargs)

    def __ge__(self, other, *args, **kwargs):
        return self.__run_comparator('__ge__', other, *args, **kwargs)

    def __le__(self, other, *args, **kwargs):
        return self.__run_comparator('__le__', other, *args, **kwargs)

    def __neg__(self, *args, **kwargs):
        return Number(super().__neg__(*args, **kwargs))

    def __repr__(self):
        return "Number('%s')" % str(self)

    def __str__(self, *args, **kwargs) -> str:
        if self == Number(0):
            return '0'
        return super().__str__(*args, **kwargs).rstrip('0').rstrip('.')

    def __format__(self, *args, **kwargs) -> str:
        if self == Number(0):
            return '0'
        return super().__format__(*args, **kwargs).rstrip('0').rstrip('.')

    def __run_operator(self, operator_name, value, *args, **kwargs):
        other = Number(value)
        operator = getattr(super(), operator_name)
        res = operator(other, *args, **kwargs)
        return Number(res)

    def __run_comparator(self, operator_name, value):
        other = Number(value)
        operator = getattr(super(), operator_name)
        return operator(other)

    def _round(self, ctx, type_: PrecisionType) -> 'Number':
        if ctx is None:
            raise Exception('Not available round for Number without context')

        prec = DEFAULT_PRECISION
        exp = decimal.Decimal(str(10**-prec))
        value = self.quantize(exp, rounding=decimal.ROUND_DOWN)
        value = str(value)
        value = decimal.Decimal.__new__(Number, value)
        return value

    def round(self, prec=DEFAULT_PRECISION, rounding=ROUND_DOWN):
        exp = decimal.Decimal(str(10**-prec))
        value = self.quantize(exp, rounding=rounding)
        value = str(value)
        value = decimal.Decimal.__new__(Number, value)
        return value

    def round_amount(self, ctx: Context) -> 'Number':
        return self._round(ctx, PrecisionType.AMOUNT)

    def round_cost(self, ctx: Context) -> 'Number':
        return self._round(ctx, PrecisionType.COST)

    def round_price(self, ctx: Context) -> 'Number':
        return self._round(ctx, PrecisionType.PRICE)


class ConstrainedNumber(Number, metaclass=ConstrainedNumberMeta):
    """
    Поддержка валидаций pydantic
    """

    gt: OptionalIntFloatDecimal = None
    ge: OptionalIntFloatDecimal = None
    lt: OptionalIntFloatDecimal = None
    le: OptionalIntFloatDecimal = None
    max_digits: OptionalInt = None
    decimal_places: OptionalInt = None
    multiple_of: OptionalIntFloatDecimal = None

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        return pydantic.ConstrainedDecimal.__modify_schema__(field_schema)

    @classmethod
    def __get_validators__(cls):
        def number_validator(v: Any) -> Number:
            return Number(decimal_validator(v))

        yield number_validator
        yield number_size_validator
        yield number_multiple_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: Number) -> Number:
        return pydantic.ConstrainedDecimal.validate(value)


def connumber(
    *,
    gt: Number = None,
    ge: Number = None,
    lt: Number = None,
    le: Number = None,
    max_digits: int = None,
    decimal_places: int = None,
    multiple_of: Number = None,
) -> Type[Number]:
    """
    Поддержка валидаций pydantic
    """
    namespace = dict(
        gt=gt, ge=ge, lt=lt, le=le, max_digits=max_digits, decimal_places=decimal_places, multiple_of=multiple_of
    )
    return type('ConstrainedNumberValue', (ConstrainedNumber,), namespace)
