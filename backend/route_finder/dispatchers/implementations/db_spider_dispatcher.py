from typing import Type

from backend.google_api.google_route_objects import RouteLeg
from backend.route_finder.dispatchers.base_spider_dispatcher import BaseSpiderDispatcher
from backend.spiders.implementations.db_sipder import DBSpider
from backend.spiders.spider_base import BaseSpider


class DbSpiderDispatcher(BaseSpiderDispatcher):
    def dispatch_spider(self, leg: RouteLeg) -> Type[BaseSpider] | None:
        return DBSpider
