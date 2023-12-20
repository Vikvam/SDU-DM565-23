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
from backend.route_finder.route_finder import RouteFinder

if __name__ == "__main__":
    logging.basicConfig(**get_logging_settings())
    configure_logging(install_root_handler=False)

    departure = "Odense"
    arrival = "Munich"
    departure_datetime = "2024-01-31T00:00:00Z"

    google_geocoding = GoogleGeocoding(get_settings().google_maps_api_key)
    nearest_airport_finder = NearestAirportFinder(get_settings().skyscanner_api_key, google_geocoding)
    flight_finder = SkyscannerFlightFinder(get_settings().skyscanner_api_key)
    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key, nearest_airport_finder, flight_finder)

    main_dispatcher = MainSpiderDispatcher()
    crawler_process = CrawlerProcess(get_pipeline_crawler_process_settings(), install_root_handler=False)
    name_resolvers = [OpenStreetMapNameResolver()]
    finder = RouteFinder(google_finder, main_dispatcher, crawler_process, name_resolvers)

    routes = finder.find_routes(departure, arrival, departure_datetime)
    print(routes)
