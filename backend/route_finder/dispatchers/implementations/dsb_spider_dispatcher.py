import urllib
from typing import Type

import requests

from backend.google_api.google_route_objects import RouteLeg, RoutePlaceDetails
from backend.route_finder.dispatchers.base_spider_dispatcher import BaseSpiderDispatcher
from backend.spiders.implementations.dsb_denmark_spider import DsbDenmarkSpider
from backend.spiders.implementations.dsb_europe_spider import DsbEuropeSpider
from backend.spiders.spider_base import BaseSpider


class DsbSpiderDispatcher(BaseSpiderDispatcher):
    _url = "https://nominatim.openstreetmap.org/reverse?"
    _url_params_longitude_key = "lon"
    _url_params_latitude_key = "lat"
    _url_params_zoom_value_country_details = 3
    _url_params = {
        _url_params_longitude_key: None,
        _url_params_latitude_key: None,
        "format": "json",
        "zoom": _url_params_zoom_value_country_details,
        "addressdetails": 0,
        "extratags": 0
    }

    def dispatch_spider(self, leg: RouteLeg) -> Type[BaseSpider]:
        departure_country = self._send_reverse_request(leg.departure)
        arrival_country = self._send_reverse_request(leg.arrival)

        if arrival_country == departure_country:
            return DsbDenmarkSpider
        else:
            return DsbEuropeSpider

    def _send_reverse_request(self, place: RoutePlaceDetails) -> str:
        params = self._url_params.copy()
        params[self._url_params_longitude_key] = place.longitude
        params[self._url_params_latitude_key] = place.latitude
        return self._send_request(params)['name']

    def _send_request(self, params) -> dict:
        url = self._url + urllib.parse.urlencode(params)
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
