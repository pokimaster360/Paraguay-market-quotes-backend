from dataclasses import dataclass, field
from datetime import datetime

from .Trend import Trend
from .exchange_type import ExchangeType

@dataclass
class Currency:
    house: str
    name: str
    buy: str | None
    sell: str | None
    buy_trend: Trend | None
    sell_trend: Trend | None
    exchange_type: ExchangeType = ExchangeType.CASH
    created_at: datetime = field(default_factory = datetime.now)