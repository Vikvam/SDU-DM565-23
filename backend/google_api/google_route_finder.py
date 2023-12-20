from datetime import date, timedelta
from enum import Enum, auto

import requests

from backend.flights.nereast_airport_finder import NearestAirportFinder
from backend.flights.skyscanner_flight_finder import SkyscannerFlightFinder, SkyscannerRequest, QueryLeg
from backend.google_api.datetime_converter import combine_date_with_time, convert_datetime_to_str, \
    convert_str_to_datetime
from backend.google_api.google_route_objects import (ResponseBody, RouteLegTransitAgency,
                                                     RouteLegTransitLine, RouteLeg, Route, RoutePlaceDetails)


class GoogleDatetimeOption(Enum):
    DEPARTURE_TIME = auto()
    ARRIVAL_TIME = auto


class GoogleRouteFinder:
    request_headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": "",
        "X-Goog-FieldMask": "routes.legs.steps.transitDetails"
    }

    request_body = {
        "origin": {
            "address": ""
        },
        "destination": {
            "address": ""
        },
        "travelMode": "TRANSIT",
        "computeAlternativeRoutes": "",
        "languageCode": "en-GB",
        "units": "METRIC"
    }

    GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

    def __init__(self, api_key, nearest_airport_finder: NearestAirportFinder,
                 skyscanner_flight_finder: SkyscannerFlightFinder):
        self.request_headers["X-Goog-Api-Key"] = api_key
        self._airport_finder = nearest_airport_finder
        self._flight_finder = skyscanner_flight_finder

    def find_routes(self, start_address: str, end_address: str, journey_datetime: str,
                    datetime_option: GoogleDatetimeOption = GoogleDatetimeOption.DEPARTURE_TIME,
                    should_compute_alternate_routes: bool = True,
                    should_include_flights: bool = False):
        self.request_body["origin"]["address"] = start_address
        self.request_body["destination"]["address"] = end_address

        if datetime_option == GoogleDatetimeOption.DEPARTURE_TIME:
            self.request_body["departureTime"] = journey_datetime
            if "arrivalTime" in self.request_body:
                del self.request_body["arrivalTime"]
        else:
            self.request_body["arrivalTime"] = journey_datetime
            if "departureTime" in self.request_body:
                del self.request_body["departureTime"]

        self.request_body['computeAlternativeRoutes'] = "true" if should_compute_alternate_routes else "false"

        try:
            result = self._send_request()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        result = GoogleRouteFinder._clean_response_body(result.json())
        routes = GoogleRouteFinder._convert_response_body_to_routes(result)

        if should_include_flights:
            routes.append(
                self._compute_flight_route(start_address, end_address,
                                           convert_str_to_datetime(journey_datetime).date()))

        return ResponseBody(start_address, end_address, routes)

    def _send_request(self):
        result = requests.post(self.GOOGLE_ROUTES_URL, json=self.request_body, headers=self.request_headers)
        result.raise_for_status()
        return result

    @staticmethod
    def _clean_response_body(response_body):
        response_body = GoogleRouteFinder._clean_data(response_body)
        response_body = GoogleRouteFinder._remove_response_body_nesting(response_body)
        return response_body

    @staticmethod
    def _clean_data(data):
        new_dict = {}

        if data:
            for key, value in data.items():
                if isinstance(value, dict):
                    value = GoogleRouteFinder._clean_data(value)
                elif isinstance(value, list):
                    new_list = []

                    for item in value:
                        item = GoogleRouteFinder._clean_data(item)
                        if item is not None:
                            new_list.append(item)

                    value = new_list

                if value not in ("", None, {}, []):
                    new_dict[key] = value

            if new_dict == {}:
                return None
            else:
                return new_dict

        return None

    @staticmethod
    def _remove_response_body_nesting(data):
        for route in data['routes']:
            route['legs'] = route['legs'][0]['steps']

        return data

    @staticmethod
    def _convert_response_body_to_routes(response_body):
        routes = []

        for item in response_body['routes']:
            route_legs = []

            for leg in item['legs']:
                leg = GoogleRouteFinder._convert_to_route_leg(leg)
                route_legs.append(leg)

            routes.append(Route(route_legs))

        return routes

    @staticmethod
    def _convert_to_route_leg(leg):
        transit_details = leg['transitDetails']
        stop_details = transit_details['stopDetails']
        localized_values = transit_details['localizedValues']

        departure = GoogleRouteFinder._get_place_from_route_leg(stop_details['departureStop'])
        arrival = GoogleRouteFinder._get_place_from_route_leg(stop_details['arrivalStop'])

        departure_datetime = combine_date_with_time(
            stop_details['departureTime'],
            GoogleRouteFinder._get_time_from_localized_values(localized_values, 'departureTime')
        )

        arrival_datetime = combine_date_with_time(
            stop_details['arrivalTime'],
            GoogleRouteFinder._get_time_from_localized_values(localized_values, 'arrivalTime')
        )

        transit_line = GoogleRouteFinder._convert_transit_line_to_object(transit_details['transitLine'])

        return RouteLeg(departure, arrival, departure_datetime, arrival_datetime, transit_line)

    @staticmethod
    def _get_place_from_route_leg(stop_details_stop):
        departure_place_name = stop_details_stop['name']
        departure_longitude = stop_details_stop['location']['latLng']['longitude']
        departure_latitude = stop_details_stop['location']['latLng']['latitude']
        return RoutePlaceDetails(departure_place_name, departure_longitude, departure_latitude)

    @staticmethod
    def _get_time_from_localized_values(localized_values, direction):
        return localized_values[direction]['time']['text']

    @staticmethod
    def _convert_transit_line_to_object(transit_line):
        if "nameShort" in transit_line:
            line_name = transit_line['nameShort']
        else:
            line_name = transit_line['name']

        vehicle_type = transit_line['vehicle']['name']['text']
        transit_agencies = [RouteLegTransitAgency(t['name'], t['uri']) for t in transit_line['agencies']]
        return RouteLegTransitLine(line_name, vehicle_type, transit_agencies)

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
        route_leg_to_airport = self.find_routes(start_address,
                                                flight_route_leg.departure.name,
                                                convert_datetime_to_str(arrival_to_airport_datetime),
                                                GoogleDatetimeOption.ARRIVAL_TIME, False)
        return route_leg_to_airport.routes[0].legs

    def _compute_route_leg_from_arrival_airport(self, end_address: str, flight_route_leg: RouteLeg) -> list[RouteLeg]:
        departure_minutes_after_flight = 30

        departure_from_airport_datetime = (flight_route_leg.arrival_datetime +
                                           timedelta(minutes=departure_minutes_after_flight))
        route_leg_from_airport = self.find_routes(flight_route_leg.arrival.name,
                                                  end_address,
                                                  convert_datetime_to_str(departure_from_airport_datetime))
        return route_leg_from_airport.routes[0].legs
