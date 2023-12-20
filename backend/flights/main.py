from datetime import date

from backend.config import get_settings
from backend.flights.nereast_airport_finder import NearestAirportFinder
from backend.flights.skyscanner_flight_finder import SkyscannerFlightFinder, SkyscannerRequest, QueryLeg
from backend.google_api.google_geocoding import GoogleGeocoding

if __name__ == "__main__":
    departure = 'Berlin Hbf'
    arrival = 'Copenhagen'

    google_geocoding = GoogleGeocoding(get_settings().google_maps_api_key)
    finder = NearestAirportFinder(get_settings().skyscanner_api_key, google_geocoding)

    departure_airport = finder.find_nearest_airport(departure)
    arrival_airport = finder.find_nearest_airport(arrival)

    api = SkyscannerFlightFinder(get_settings().skyscanner_api_key)
    request = SkyscannerRequest(
        query_legs=[QueryLeg(departure_airport.iata_code, arrival_airport.iata_code, date(2023, 12, 20))])
    result = api.get(request)
    print(result)
