import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from backend.config import get_settings, get_pipeline_crawler_process_settings, get_logging_settings
from backend.flights.nereast_airport_finder import NearestAirportFinder
from backend.flights.skyscanner_flight_finder import SkyscannerFlightFinder
from backend.google_api.google_geocoding import GoogleGeocoding
from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.name_resolvers.openstreet_name_resolver import OpenStreetMapNameResolver
from backend.route_finder.dispatchers.main_spider_dispatcher import MainSpiderDispatcher
from backend.route_finder.flight_appender import FlightAppender
from backend.route_finder.route_finder import RouteFinder

if __name__ == "__main__":
    logging.basicConfig(**get_logging_settings())
    configure_logging(install_root_handler=False)

    departure = "København H"
    arrival = "Berlin Hbf"
    departure_datetime = "2023-12-27T00:00:00Z"

    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    google_geocoding = GoogleGeocoding(get_settings().google_maps_api_key)
    nearest_airport_finder = NearestAirportFinder(get_settings().skyscanner_api_key, google_geocoding)
    flight_finder = SkyscannerFlightFinder(get_settings().skyscanner_api_key)
    flight_appender = FlightAppender(google_finder, nearest_airport_finder, flight_finder)
    main_dispatcher = MainSpiderDispatcher()
    crawler_process = CrawlerProcess(get_pipeline_crawler_process_settings(), install_root_handler=False)
    name_resolvers = [OpenStreetMapNameResolver()]
    finder = RouteFinder(google_finder, flight_appender, main_dispatcher, crawler_process, name_resolvers)

    routes = finder.find_routes(departure, arrival, departure_datetime, True)
    print(routes)
