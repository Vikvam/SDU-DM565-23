import datetime
import logging

from scrapy.crawler import CrawlerProcess

from backend.config import get_settings, get_pipeline_crawler_process_settings, get_logging_settings
from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.name_resolvers.openstreet_name_resolver import OpenStreetMapNameResolver
from backend.route_finder.dispatchers.implementations.dsb_spider_dispatcher import DsbSpiderDispatcher
from backend.route_finder.dispatchers.implementations.flixbus_spider_dispatcher import FlixbusSpiderDispatcher
from backend.route_finder.route_finder import RouteFinder

dispatchers = [
    {
        "travel_agency": "flixbus",
        "dispatcher": FlixbusSpiderDispatcher()
    },
    {
        "travel_agency": "dsb",
        "dispatcher": DsbSpiderDispatcher()
    }
]

if __name__ == "__main__":
    logging.basicConfig(**get_logging_settings())
    logger = logging.getLogger(__name__)

    departure = "Odense"
    arrival = "Munich"
    departure_datetime = datetime.datetime(2023, 12, 27, 16, 30)

    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    crawler_process = CrawlerProcess(get_pipeline_crawler_process_settings())
    name_resolvers = [OpenStreetMapNameResolver()]
    finder = RouteFinder(google_finder, dispatchers, crawler_process, name_resolvers)

    routes = finder.find_routes(departure, arrival, departure_datetime)
    print(routes)
