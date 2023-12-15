from abc import ABC
from dataclasses import dataclass
from datetime import datetime

import scrapy
from money import Money


@dataclass
class SpiderRequest:
    departure_place: str
    arrival_place: str
    departure_datetime: datetime


@dataclass
class SpiderItem:
    departure_place: str
    arrival_place: str
    departure_datetime: datetime
    arrival_date_time: datetime
    price: Money
    transport_agent_name: str


class BaseSpider(scrapy.Spider, ABC):
    name: str

    def __init__(self, travel_agency: str, request: SpiderRequest, **kwargs):
        super().__init__(**kwargs)
        self._travel_agency = travel_agency
        self._request = request