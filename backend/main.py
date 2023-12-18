import datetime
import logging

from scrapy.crawler import CrawlerProcess

from backend.config import get_settings, get_pipeline_crawler_process_settings, get_logging_settings
from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.name_resolvers.openstreet_name_resolver import OpenStreetMapNameResolver
from backend.route_finder.route_finder import RouteFinder

if __name__ == "__main__":
    logging.basicConfig(**get_logging_settings())
    logger = logging.getLogger(__name__)

    departure = "University of Southern Denmark, SDU"
    arrival = "ZOB Hamburg"

    departure_datetime = datetime.datetime(2023, 12, 19, 16, 30)
    departure_datetime = datetime.datetime(2023, 12, 16, 16, 30)

    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    crawler_process = CrawlerProcess(get_pipeline_crawler_process_settings())
    name_resolvers = [OpenStreetMapNameResolver()]
    finder = RouteFinder(google_finder, crawler_process, name_resolvers)

    routes = finder.find_routes(departure, arrival, departure_datetime)
    print(routes)
