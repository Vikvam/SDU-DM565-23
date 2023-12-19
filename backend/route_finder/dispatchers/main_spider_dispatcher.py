from dataclasses import dataclass
from typing import Type

from backend.google_api.google_route_objects import RouteLeg, RouteLegTransitAgency
from backend.route_finder.dispatchers.base_spider_dispatcher import BaseSpiderDispatcher
from backend.route_finder.dispatchers.implementations.db_spider_dispatcher import DbSpiderDispatcher
from backend.route_finder.dispatchers.implementations.dsb_spider_dispatcher import DsbSpiderDispatcher
from backend.route_finder.dispatchers.implementations.flixbus_spider_dispatcher import FlixbusSpiderDispatcher
from backend.spiders.spider_base import BaseSpider


@dataclass
class DispatcherConnector:
    travel_agency_name: str
    travel_agency_url: str
    dispatcher: BaseSpiderDispatcher


class MainSpiderDispatcher(BaseSpiderDispatcher):
    connectors = [
        DispatcherConnector("flixbus", "https://global.flixbus.com/", FlixbusSpiderDispatcher()),
        DispatcherConnector("dsb", "http://www.dsb.dk/", DsbSpiderDispatcher()),
        #DispatcherConnector("db", "https://www.bahn.de/", DbSpiderDispatcher())
    ]

    def dispatch_spider(self, leg: RouteLeg) -> Type[BaseSpider] | None:
        agency_urls = self._get_transit_agency_urls(leg.transit_line.transit_agencies)
        agency_names = self._get_transit_agency_names(leg.transit_line.transit_agencies)

        for connector in self.connectors:
            if connector.travel_agency_name in agency_names or connector.travel_agency_url in agency_urls:
                return connector.dispatcher.dispatch_spider(leg)
        return None

    @staticmethod
    def _get_transit_agency_urls(agencies: list[RouteLegTransitAgency]) -> list[str]:
        return [i.uri.lower() for i in agencies]

    @staticmethod
    def _get_transit_agency_names(agencies: list[RouteLegTransitAgency]) -> list[str]:
        return [i.name.lower() for i in agencies]
