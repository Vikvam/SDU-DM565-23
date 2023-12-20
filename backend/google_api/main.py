from datetime import datetime

from backend.config import get_settings
from backend.flights.nereast_airport_finder import NearestAirportFinder
from backend.flights.skyscanner_flight_finder import SkyscannerFlightFinder
from backend.google_api.datetime_converter import convert_datetime_to_str
from backend.google_api.google_geocoding import GoogleGeocoding
from google_route_finder import GoogleRouteFinder

start_address = "Copenhagen Central Station"
end_address = "Berlin Hbf"


def main():
    google_geocoding = GoogleGeocoding(get_settings().google_maps_api_key)
    nearest_airport_finder = NearestAirportFinder(get_settings().skyscanner_api_key, google_geocoding)
    flight_finder = SkyscannerFlightFinder(get_settings().skyscanner_api_key)
    route_finder = GoogleRouteFinder(get_settings().google_maps_api_key, nearest_airport_finder, flight_finder)

    result = route_finder.find_routes(start_address,
                                      end_address,
                                      convert_datetime_to_str(datetime.now()),
                                      should_compute_alternate_routes=False, should_include_flights=True)
    print_routes(result.routes)


def print_routes(routes):
    for i, route in enumerate(routes):
        print(f"Route #{i + 1}:")

        for j, step in enumerate(route.legs):
            print(f" -> Step #{j + 1}: start: {step.departure.name}, end: {step.arrival.name}, "
                  f"line: {step.transit_line.line_name}, provider: {step.transit_line.transit_agencies[0].name}")


if __name__ == '__main__':
    main()
