import logging
from multiprocessing import Queue, Process
from typing import Type

import scrapy
from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json
from money import Money
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from backend.config import get_pipeline_crawler_process_settings
from backend.google_api.datetime_converter import convert_datetime_to_str


@dataclass
class SpiderRequest:
    departure_place: str
    arrival_place: str
    departure_datetime: datetime

    def __str__(self):
        return f"SpiderRequest(departure_place='{self.departure_place}', arrival_place='{self.arrival_place}', departure_datetime='{convert_datetime_to_str(self.departure_datetime)}'"


@dataclass
class SpiderItem:
    departure_place: str
    arrival_place: str
    departure_datetime: datetime
    arrival_datetime: datetime
    price: Money
    transport_agent_name: str

    def as_dict(self):
        return {
            "departure_place": self.departure_place,
            "arrival_place": self.arrival_place,
            "departure_datetime": convert_datetime_to_str(self.departure_datetime),
            "arrival_datetime": convert_datetime_to_str(self.arrival_datetime),
            "price": {"amount": str(self.price.amount), "currency": self.price.currency},
            "transport_agent_name": self.transport_agent_name,
        }


class BaseSpider(scrapy.Spider, ABC):
    name: str

    def __init__(self, travel_agency: str, request: SpiderRequest, timeout=4, **kwargs):
        super().__init__(**kwargs)
        self._travel_agency = travel_agency
        self._request = request
        self._timeout = timeout
        # self.settings.set("LOG_LEVEL", logging.INFO)


# Adapted from: https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable
def crawl_run_wrapper(queue: Queue, spider: Type[BaseSpider], request: SpiderRequest):
    try:
        runner = CrawlerRunner(get_pipeline_crawler_process_settings())
        deferred = runner.crawl(spider, request)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        queue.put(None)
    except Exception as e:
        queue.put(e)


# Adapted from: https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable
def run_spider(spider: Type[BaseSpider], request: SpiderRequest):
    queue = Queue()
    process = Process(target=crawl_run_wrapper, args=[queue, spider, request])
    process.start()
    result = queue.get()
    process.join()

    if result is not None:
        raise result
