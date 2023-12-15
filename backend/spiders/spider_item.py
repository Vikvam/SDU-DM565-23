from dataclasses import dataclass
from datetime import datetime

from money import Money


@dataclass
class SpiderItem:
    departure_place: str
    arrival_place: str
    departure_datetime: datetime
    arrival_date_time: datetime
    price: Money
    transport_agent_name: str
