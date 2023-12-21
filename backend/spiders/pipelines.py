import json
import logging
from datetime import datetime
from typing import Optional
from typing.io import IO

from backend.google_api.datetime_converter import convert_str_to_datetime
from backend.json_serializer import write_to_json_file
from backend.spiders.spider_base import SpiderItem, BaseSpider


class RoutePipeline:
    def __init__(self):
        self._file = None
        self._result = {}
        self._items = []
        self._filename = "items.json"

    def open_spider(self, spider: BaseSpider):
        self._file = open("result.json", "r+")
        self._result = json.load(self._file)

    def process_item(self, item: SpiderItem, spider: BaseSpider):
        print("Pipeline:", item)
        self._items.append(item.as_dict())
        for route in self._result['routes']:
            for step in route['legs']:
                if (self._is_transit_agency_name_matching(step, item) and
                        self.are_item_timestamps_matching(step, item)):
                    step['price'] = {
                        "amount": "{:.2f}".format(item.price.amount),
                        "currency:": item.price.currency
                    }
        return item

    @staticmethod
    def _is_transit_agency_name_matching(step: dict, spider_item: SpiderItem) -> bool:
        spider_item_agency_name = spider_item.transport_agent_name.lower()

        for agency in step['transit_line']['transit_agencies']:
            result_agency_name = agency['name'].lower()

            if spider_item_agency_name == result_agency_name:
                return True

        return False

    @staticmethod
    def are_item_timestamps_matching(step: dict, spider_item: SpiderItem) -> bool:
        step_departure_datetime = convert_str_to_datetime(step['departure_datetime'])
        step_arrival_datetime = convert_str_to_datetime(step['arrival_datetime'])

        return (RoutePipeline.is_time_matching(step_departure_datetime, spider_item.departure_datetime) and
                RoutePipeline.is_time_matching(step_arrival_datetime, spider_item.arrival_datetime))

    @staticmethod
    def is_time_matching(a: datetime, b: datetime) -> bool:
        return a.time() == b.time()

    def close_spider(self, spider):
        self.erase_file_content(self._file)
        write_to_json_file(self._file, self._result)
        self._file.close()

    @staticmethod
    def erase_file_content(file):
        file.seek(0)
        file.truncate(0)


class ItemPipeline:
    _FILENAME = "items.json"

    def __init__(self):
        self._file: Optional[IO] = None
        self._items = []
        self._pipeline_items = {}

    def open_spider(self, spider: BaseSpider):
        self._file = open(self._FILENAME, "r+")
        try:
            self._pipeline_items = json.load(self._file)
        except json.decoder.JSONDecodeError:
            self._pipeline_items = {}

    def process_item(self, item: SpiderItem, spider: BaseSpider):
        print("Pipeline:", item)
        self._items.append(item.as_dict())
        return item

    def close_spider(self, spider: BaseSpider):
        self.erase_file_content(self._file)
        self._pipeline_items[str(spider._request)] = self._items
        print("Pipeline items:", self._pipeline_items, type(self._pipeline_items))
        write_to_json_file(self._file, self._pipeline_items)
        self._file.close()

    @staticmethod
    def erase_file_content(file):
        file.seek(0)
        file.truncate(0)

    @classmethod
    def reset_pipeline(cls):
        with open(cls._FILENAME, "w"):
            pass
