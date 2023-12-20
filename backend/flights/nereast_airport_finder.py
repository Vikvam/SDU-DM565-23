from dataclasses import dataclass

import requests


@dataclass
class Airport:
    name: str
    iata_code: str
    longitude: str
    latitude: str


class NearestAirportFinder:
    _url = 'https://partners.api.skyscanner.net/apiservices/v3/geo/hierarchy/flights/nearest'
    _url_headers_key_api_key = 'x-api-key'
    _request_headers = {
        "Content-Type": "application/json",
        _url_headers_key_api_key: "",
    }
    _request_body = {
        'locale': 'en-GB',
        'locator': {
            'coordinates': {
                "latitude": 0.0,
                "longitude": 0.0
            }
        }
    }

    def __init__(self, skyscanner_api_key, google_geocoding):
        self._request_headers[self._url_headers_key_api_key] = skyscanner_api_key
        self._google_geocoding = google_geocoding

    def find_nearest_airport(self, address: str) -> Airport:
        address_long, address_lat = self._convert_address_to_coordinates(address)
        result = self._send_request(address_long, address_lat)

        for key, value in result['places'].items():
            if value['iata'] != '':
                return Airport(
                    value['name'],
                    value['iata'],
                    str(value['coordinates']['longitude']),
                    str(value['coordinates']['latitude'])
                )

    def _convert_address_to_coordinates(self, address: str) -> (str, str):
        return self._google_geocoding.find_coordinates(address)

    def _send_request(self, longitude: str, latitude: str) -> dict:
        request_body = self._request_body.copy()
        request_body['locator']['coordinates']['longitude'] = float(longitude)
        request_body['locator']['coordinates']['latitude'] = float(latitude)

        result = requests.post(self._url, headers=self._request_headers, json=request_body)
        result.raise_for_status()
        return result.json()
