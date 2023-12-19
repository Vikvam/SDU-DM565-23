import datetime
import logging
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from backend.config import get_settings, get_pipeline_crawler_process_settings, get_logging_settings
from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.name_resolvers.openstreet_name_resolver import OpenStreetMapNameResolver
from backend.route_finder.dispatchers.main_spider_dispatcher import MainSpiderDispatcher
from backend.route_finder.route_finder import RouteFinder


if __name__ == "__main__":
    logging.basicConfig(**get_logging_settings())
    configure_logging(install_root_handler=False)

    departure = "Odense"
    arrival = "Munich"
    departure_datetime = "2024-01-31T00:00:00Z"

    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    main_dispatcher = MainSpiderDispatcher()
    crawler_process = CrawlerProcess(get_pipeline_crawler_process_settings(), install_root_handler=False)
    name_resolvers = [OpenStreetMapNameResolver()]
    finder = RouteFinder(google_finder, main_dispatcher, crawler_process, name_resolvers)

    routes = finder.find_routes(departure, arrival, departure_datetime)
    print(routes)
