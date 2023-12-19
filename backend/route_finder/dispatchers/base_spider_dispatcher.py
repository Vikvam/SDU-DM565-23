from abc import ABC, abstractmethod
from typing import Type

from backend.google_api.google_route_objects import RouteLeg
from backend.spiders.spider_base import BaseSpider


class BaseSpiderDispatcher(ABC):
    @abstractmethod
    def dispatch_spider(self, leg: RouteLeg) -> Type[BaseSpider] | None:
        pass
