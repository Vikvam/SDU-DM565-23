import urllib

import requests


class GoogleGeocoding:
    _url = "https://maps.googleapis.com/maps/api/geocode/json?"
    _url_params = {
        "language": "en-GB",
        "address": "",
        "key": ""
    }

    def __init__(self, google_maps_api_key):
        self._url_params['key'] = google_maps_api_key

    def find_coordinates(self, address: str) -> (str, str):
        result = self._send_request(address)
        result = result['results'][0]['geometry']['location']

        return result['lng'], result['lat']

    def _send_request(self, address: str) -> dict:
        params = self._url_params.copy()
        params['address'] = address

        url = self._url + urllib.parse.urlencode(params)
        result = requests.get(url)
        result.raise_for_status()
        return result.json()
