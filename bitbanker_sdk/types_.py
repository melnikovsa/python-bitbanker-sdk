import enum


class Currency(str, enum.Enum):
    RUB = 'RUB'
    BTC = 'BTC'
    ETH = 'ETH'
