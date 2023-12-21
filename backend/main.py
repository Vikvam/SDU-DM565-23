import datetime
import logging
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from backend.config import get_settings, get_pipeline_crawler_process_settings, get_logging_settings
from backend.flights.nereast_airport_finder import NearestAirportFinder
from backend.flights.skyscanner_flight_finder import SkyscannerFlightFinder
from backend.google_api.google_geocoding import GoogleGeocoding
from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.json_serializer import write_to_json_file
from backend.name_resolvers.openstreet_name_resolver import OpenStreetMapNameResolver
from backend.route_finder.dispatchers.main_spider_dispatcher import MainSpiderDispatcher
from backend.route_finder.flight_appender import FlightAppender
from backend.route_finder.route_finder import RouteFinder
from backend.spiders.pipelines import ItemPipeline

if __name__ == "__main__":
    logging.basicConfig(**get_logging_settings())
    configure_logging(install_root_handler=False)

    # departure = "Frankfurt"
    # arrival = "Hamburg"
    # departure_datetime = "2024-01-31T00:00:00Z"

    departure = "Copenhagen"
    arrival = "Frankfurt"
    departure_datetime = "2024-01-27T00:00:00Z"

    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    google_geocoding = GoogleGeocoding(get_settings().google_maps_api_key)
    nearest_airport_finder = NearestAirportFinder(get_settings().skyscanner_api_key, google_geocoding)
    flight_finder = SkyscannerFlightFinder(get_settings().skyscanner_api_key)
    flight_appender = FlightAppender(google_finder, nearest_airport_finder, flight_finder)
    main_dispatcher = MainSpiderDispatcher()
    crawler_process = CrawlerProcess(get_pipeline_crawler_process_settings(), install_root_handler=False)
    name_resolvers = [OpenStreetMapNameResolver()]
    finder = RouteFinder(google_finder, flight_appender, main_dispatcher, crawler_process, name_resolvers)

    # ItemPipeline.reset_pipeline()
    # routes = finder.find_routes(departure, arrival, departure_datetime, should_include_flight=True)
    result = ItemPipeline.finish_pipeline()

    with open(f"{departure}-{arrival}-result.json", "w") as f:
        write_to_json_file(f, result)

    print(result)
