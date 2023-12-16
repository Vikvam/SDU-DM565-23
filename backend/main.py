import datetime
import logging
from typing import Type

from scrapy.crawler import CrawlerProcess
from twisted.internet import defer, reactor

from backend.config import get_settings, get_pipeline_crawler_process_settings
from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.google_api.google_route_objects import Route, RouteLeg, RouteLegTransitAgency
from backend.json_serializer import write_to_json_file, encode_json
from backend.name_resolvers.name_resolver_base import NameResolverBase
from backend.name_resolvers.openstreet_name_resolver import OpenStreetMapNameResolver
from backend.spiders.implementations.flixbus_spider import FlixbusSpider
from backend.spiders.spider_base import SpiderRequest, BaseSpider


@defer.inlineCallbacks
def crawl(process: CrawlerProcess, data: list[Route], name_resolvers: list[NameResolverBase]):
    for route in data:
        for step in route.legs:
            transport_agency_names = get_transit_agencies_names(step.transit_line.transit_agencies)
            spider = dispatch_spider(transport_agency_names)

            if spider is not None:
                yield crawl_route_step(process, step, spider, name_resolvers)

    reactor.stop()


@defer.inlineCallbacks
def crawl_route_step(process: CrawlerProcess, route_leg: RouteLeg,
                     spider: Type[BaseSpider], name_resolvers: list[NameResolverBase]):
    departure_names = find_place_names(route_leg.departure_place_name, name_resolvers)
    arrival_names = find_place_names(route_leg.arrival_place_name, name_resolvers)

    for i, departure_name in enumerate(departure_names):
        yield process.crawl(spider,
                            request=SpiderRequest(departure_name,
                                                  arrival_names[i],
                                                  route_leg.departure_datetime))


def get_transit_agencies_names(agencies: list[RouteLegTransitAgency]) -> list[str]:
    return [i.name.lower() for i in agencies]


def find_place_names(place_name: str, name_resolvers: list[NameResolverBase]):
    names = [place_name]

    for resolver in name_resolvers:
        names.append(resolver.find_name(place_name))

    return names


def dispatch_spider(transport_agency_names: list[str]) -> Type[FlixbusSpider]:
    spiders = {
        "flixbus": FlixbusSpider
    }

    for name, value in spiders.items():
        if name in transport_agency_names:
            return value


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    departure = "University of Southern Denmark, SDU"
    arrival = "ZOB Hamburg"
    departure_datetime = datetime.datetime(2023, 12, 16, 16, 30)

    logger.info(f"Searching... ('{departure}', '{arrival}', {departure_datetime})")

    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    result = google_finder.find_routes(departure, arrival, departure_datetime)
    # result = aux_result # use to skip the previous computations
    json_result = encode_json(result)

    with open("result.json", "w") as out:
        write_to_json_file(out, json_result)

    crawler_process = CrawlerProcess(
        get_pipeline_crawler_process_settings()
    )

    resolvers = [OpenStreetMapNameResolver()]

    crawl(crawler_process, result.routes, resolvers)
    reactor.run()

    # with open("result.json", "r") as f:
    #     print(f.read())
