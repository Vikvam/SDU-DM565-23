import urllib

import requests

from backend.name_resolvers.name_resolver_base import NameResolverBase


class OpenStreetMapNameResolver(NameResolverBase):
    _url = "https://nominatim.openstreetmap.org/search?"
    _url_params_place_name_key = "q"
    _url_params = {
        "format": "json",
        "namedetails": 1,
        _url_params_place_name_key: ""
    }

    def find_name(self, item: str) -> str | None:
        params = self.add_place_name_to_url_params(item)

        try:
            result = self._send_request(params)
        except requests.exceptions.HTTPError:
            return None

        return self._retrieve_place_name_from_result(result)

    def add_place_name_to_url_params(self, name: str) -> dict:
        params = self._url_params.copy()
        params[self._url_params_place_name_key] = name
        return params

    def _send_request(self, params) -> dict:
        url = self._url + urllib.parse.urlencode(params)
        res = requests.get(url)
        res.raise_for_status()
        return res.json()

    @staticmethod
    def _retrieve_place_name_from_result(result: list) -> str | None:
        if len(result) == 0:
            return None

        place = OpenStreetMapNameResolver._get_place_of_highest_importance(result)
        place = place["namedetails"]
        if "official_name" in result:
            return place["official_name"]
        else:
            return place["name"]

    @staticmethod
    def _get_place_of_highest_importance(result: list) -> dict:
        return sorted(result, key=lambda item: float(item['importance']), reverse=True)[0]
