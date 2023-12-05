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

        route = ResponseBody(**result.json())
        print(route)

        print(result.json())

    def send_request(self):
        result = requests.post(self.GOOGLE_ROUTES_URL, json=self.request_body, headers=self.request_headers)
        result.raise_for_status()
        return result
