from datetime import datetime

import requests

from google_route_objects import ResponseBody, RouteLegTransitAgency, RouteLegTransitLine, RouteLeg, Route


class GoogleRouteFinder:
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"

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
        "departureTime": "",
        "travelMode": "TRANSIT",
        "computeAlternativeRoutes": "true",
        "languageCode": "en-GB",
        "units": "METRIC"
    }

    GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

    def __init__(self, api_key):
        self.request_headers["X-Goog-Api-Key"] = api_key

    def find_routes(self, start_address, end_address, departure_time):
        self.request_body["origin"]["address"] = start_address
        self.request_body["destination"]["address"] = end_address
        self.request_body["departureTime"] = departure_time.strftime(self.datetime_format)

        try:
            result = self._send_request()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        result = GoogleRouteFinder._clean_response_body(result.json())
        routes = GoogleRouteFinder._convert_response_body_to_routes(result)
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

        departure_place_name = stop_details['departureStop']['name']
        arrival_place_name = stop_details['arrivalStop']['name']
        departure_datetime = GoogleRouteFinder._convert_to_datetime(
            stop_details['departureTime'],
            GoogleRouteFinder._get_time_from_localized_values(localized_values, 'departureTime')
        )
        arrival_datatime = GoogleRouteFinder._convert_to_datetime(
            stop_details['arrivalTime'],
            GoogleRouteFinder._get_time_from_localized_values(localized_values, 'arrivalTime')
        )
        transit_line = GoogleRouteFinder._convert_transit_line_to_object(transit_details['transitLine'])

        return RouteLeg(departure_place_name, arrival_place_name, departure_datetime, arrival_datatime, transit_line)

    @staticmethod
    def _get_time_from_localized_values(localized_values, direction):
        return localized_values[direction]['time']['text']

    @staticmethod
    def _convert_to_datetime(timestamp, localized_time):
        date_time = datetime.strptime(timestamp, GoogleRouteFinder.datetime_format)
        localized_time = date_time.strptime(localized_time, "%H:%M")
        date_time.replace(hour=localized_time.hour)
        return date_time

    @staticmethod
    def _convert_transit_line_to_object(transit_line):
        line_name = transit_line['nameShort']
        vehicle_type = transit_line['vehicle']['name']['text']
        transit_agencies = [RouteLegTransitAgency(t['name'], t['uri']) for t in transit_line['agencies']]
        return RouteLegTransitLine(line_name, vehicle_type, transit_agencies)
