import copy
from datetime import date, timedelta

from backend.flights.nereast_airport_finder import NearestAirportFinder
from backend.flights.skyscanner_flight_finder import SkyscannerFlightFinder, SkyscannerRequest, QueryLeg
from backend.google_api.datetime_converter import convert_datetime_to_str
from backend.google_api.google_route_finder import GoogleRouteFinder, GoogleDatetimeOption
from backend.google_api.google_route_objects import ResponseBody, Route, RouteLeg


class FlightAppender:
    def __init__(self, google_route_finder: GoogleRouteFinder,
                 nearest_airport_finder: NearestAirportFinder,
                 skyscanner_flight_finder: SkyscannerFlightFinder):
        self._route_finder = google_route_finder
        self._airport_finder = nearest_airport_finder
        self._flight_finder = skyscanner_flight_finder

    def append_flight_route(self, response_body: ResponseBody) -> ResponseBody:
        data = copy.deepcopy(response_body)

        if data.journey_datetime_option == GoogleDatetimeOption.ARRIVAL_TIME:
            raise Exception("Unable to compute the flight route for ARRIVAL_TIME option")

        flight_route = self._compute_flight_route(data.origin_address, data.destination_address,
                                                  data.journey_datetime)
        data.routes.append(flight_route)
        return data

    def _compute_flight_route(self, start_address: str, end_address: str, departure_date: date) -> Route:
        departure_airport = self._airport_finder.find_nearest_airport(start_address)
        arrival_airport = self._airport_finder.find_nearest_airport(end_address)

        flight_request = SkyscannerRequest(query_legs=[QueryLeg(departure_airport.iata_code,
                                                                arrival_airport.iata_code,
                                                                departure_date)])
        flight_route_leg = self._flight_finder.get(flight_request)
        route_leg_to_departure_airport = self._compute_route_leg_to_departure_airport(start_address, flight_route_leg)
        route_leg_from_arrival_airport = self._compute_route_leg_from_arrival_airport(end_address, flight_route_leg)

        route_legs = []
        route_legs.extend(route_leg_to_departure_airport)
        route_legs.append(flight_route_leg)
        route_legs.extend(route_leg_from_arrival_airport)

        return Route(route_legs)

    def _compute_route_leg_to_departure_airport(self, start_address: str, flight_route_leg: RouteLeg) -> list[RouteLeg]:
        departure_hours_before_flight = 2

        arrival_to_airport_datetime = (flight_route_leg.departure_datetime
                                       - timedelta(hours=departure_hours_before_flight))
        route_leg_to_airport = self._route_finder.find_routes(start_address,
                                                              flight_route_leg.departure.name,
                                                              convert_datetime_to_str(arrival_to_airport_datetime),
                                                              GoogleDatetimeOption.ARRIVAL_TIME, False)
        return route_leg_to_airport.routes[0].legs

    def _compute_route_leg_from_arrival_airport(self, end_address: str, flight_route_leg: RouteLeg) -> list[RouteLeg]:
        departure_minutes_after_flight = 30

        departure_from_airport_datetime = (flight_route_leg.arrival_datetime +
                                           timedelta(minutes=departure_minutes_after_flight))
        route_leg_from_airport = self._route_finder.find_routes(flight_route_leg.arrival.name,
                                                                end_address,
                                                                convert_datetime_to_str(
                                                                    departure_from_airport_datetime)
                                                                )
        return route_leg_from_airport.routes[0].legs
