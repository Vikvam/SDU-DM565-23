import json
import logging
from datetime import datetime
from itertools import product
from typing import Type

from scrapy.crawler import CrawlerProcess
from twisted.internet import defer, reactor

from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.google_api.google_route_objects import ResponseBody, Route, RouteLeg, RouteLegTransitAgency
from backend.json_serializer import encode_json, write_to_json_file
from backend.name_resolvers.name_resolver_base import NameResolverBase
from backend.spiders.spider_base import BaseSpider, SpiderRequest


class RouteFinder:
    _FILE_NAME = "result.json"

    def __init__(self, google_route_finder: GoogleRouteFinder, dispatchers: list,
                 crawler_process: CrawlerProcess, name_resolvers: list[NameResolverBase]):
        self._logger = logging.getLogger()
        self._google_route_finder = google_route_finder
        self._dispatchers = dispatchers
        self._name_resolvers = name_resolvers
        self._crawler_process = crawler_process

    def find_routes(self, departure: str, arrival: str, departure_datetime: datetime) -> dict:
        self._logger.info(f"Searching... ('{departure}', '{arrival}', {departure_datetime})")

        result = self._google_route_finder.find_routes(departure, arrival, departure_datetime)
        self._write_result_to_file(result)

        self._crawl(result.routes)
        reactor.run()

        return self._fetch_result_from_file()

    def _write_result_to_file(self, result: ResponseBody):
        json_result = encode_json(result)
        with open(self._FILE_NAME, "w") as out:
            write_to_json_file(out, json_result)

    @defer.inlineCallbacks
    def _crawl(self, routes: list[Route]):
        for route in routes:
            for step in route.legs:
                # transport_agency_names = self._get_transit_agencies_names(step.transit_line.transit_agencies)
                spider = self._dispatch_spider(step)

                if spider:
                    yield self._crawl_route_step(step, spider)

                # for spider in spiders:
                #    yield self._crawl_route_step(step, spider)

        reactor.stop()

    @defer.inlineCallbacks
    def _crawl_route_step(self, route_leg: RouteLeg, spider: Type[BaseSpider]):
        departure_names = self._find_place_names(route_leg.departure.name)
        arrival_names = self._find_place_names(route_leg.arrival.name)
        journey_names = list(product(departure_names, arrival_names))

        for departure, arrival in journey_names:
            yield self._crawler_process.crawl(spider,
                                              request=SpiderRequest(departure, arrival, route_leg.departure_datetime))

    def _find_place_names(self, place_name: str):
        names = [place_name]

        for resolver in self._name_resolvers:
            names.append(resolver.find_name(place_name))

        return names

    def _dispatch_spider(self, leg: RouteLeg) -> Type[BaseSpider] | None:
        transit_agency_names = self._get_transit_agencies_names(leg.transit_line.transit_agencies)

        for dispatcher in self._dispatchers:
            if dispatcher['travel_agency'].lower() in transit_agency_names:
                return dispatcher['dispatcher'].dispatch_spider(leg)

        return None

    @staticmethod
    def _get_transit_agencies_names(agencies: list[RouteLegTransitAgency]) -> list[str]:
        return [i.name.lower() for i in agencies]

    # @staticmethod
    # def _dispatch_spider(transport_agency_names: list[str]) -> list[Type[FlixbusSpider]]:
    #     spiders_dict = {
    #         "flixbus": [FlixbusSpider],
    #         "dsb": [DsbDenmarkSpider, DsbEuropeSpider],
    #     }
    #
    #     spiders = []
    #
    #     for name, value in spiders_dict.items():
    #         if name in transport_agency_names:
    #             spiders = value
    #
    #     return spiders

    def _fetch_result_from_file(self) -> dict:
        with open(self._FILE_NAME) as file:
            return json.load(file)
