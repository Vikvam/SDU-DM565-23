import json
import logging
from datetime import datetime
from typing import Optional
from typing.io import IO

from backend.google_api.datetime_converter import convert_str_to_datetime
from backend.json_serializer import write_to_json_file
from backend.spiders.spider_base import SpiderItem, BaseSpider, SpiderRequest


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
        self._items.append(item.as_dict())
        return item

    def close_spider(self, spider: BaseSpider):
        self.erase_file_content(self._file)
        self._pipeline_items[str(spider._request)] = self._items
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

    @classmethod
    def finish_pipeline(cls) -> dict:
        def is_item_matching_leg(item, leg):
            # print(item["departure_datetime"], leg["departure_datetime"])
            # print(item["departure_datetime"], leg["departure_datetime"])
            return item["departure_datetime"] == leg["departure_datetime"] and item["departure_datetime"] == leg["departure_datetime"]

        with open(cls._FILENAME, "r") as f: pipeline_items = json.load(f)
        with open("result.json", "r") as f: result = json.load(f)
        print(pipeline_items)
        print(result)
        for route in result["routes"]:
            for leg in route["legs"]:
                request = SpiderRequest(
                    leg["departure"]["name"],
                    leg["arrival"]["name"],
                    datetime.fromisoformat(leg["departure_datetime"]),
                )
                try:
                    for item in pipeline_items[str(request)]:
                        if is_item_matching_leg(item, leg):
                            print(f"Price for request {request} is {item['price']}")
                            leg["price"] = item["price"]
                            break
                    if not leg["price"]:
                        print(f"No item matches for {leg}")
                except KeyError:
                    print(f"Could not find item for {request}")
        return pipeline_items


