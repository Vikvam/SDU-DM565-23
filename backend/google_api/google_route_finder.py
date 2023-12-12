import requests

from google_route_objects import ResponseBody


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
        "computeAlternativeRoutes": "false",
        "languageCode": "en-GB",
        "units": "METRIC"
    }

    GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

    def __init__(self, api_key):
        self.request_headers["X-Goog-Api-Key"] = api_key

    def find_routes(self, start_address, end_address):
        self.request_body["origin"]["address"] = start_address
        self.request_body["destination"]["address"] = end_address

        try:
            result = self.send_request()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


        result = GoogleRouteFinder._clean_response_body(result.json())
        print(result)

        # route = ResponseBody(**result.json())
        # print(route)

        # print(result.json())

    def send_request(self):
        result = requests.post(self.GOOGLE_ROUTES_URL, json=self.request_body, headers=self.request_headers)
        result.raise_for_status()
        return result

    @staticmethod
    def _clean_response_body(response_body):
        response_body = GoogleRouteFinder._clean_data(response_body)
        response_body = GoogleRouteFinder.remove_response_body_nesting(response_body)
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
    def remove_response_body_nesting(data):
        for route in data['routes']:
            route['legs'] = route['legs'][0]['steps']

        return data
