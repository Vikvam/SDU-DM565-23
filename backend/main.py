import json
import urllib.parse

import requests
from fastapi.encoders import jsonable_encoder
from scrapy.crawler import CrawlerProcess
from twisted.internet import defer, reactor

from backend.config import get_settings, get_crawler_process_settings

from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.spiders.flixbus_spider import FlixbusSpider, FlixbusRequest
from backend.temp_result import result

open_street_map_url = "https://nominatim.openstreetmap.org/search?"
open_street_map_url_params = {
    "format": "json",
    "namedetails": 1,
    "limit": 1,
    "amenity": ""
}


def convert_place_names_to_official(result):
    for route in result.routes:
        for step in route.legs:
            official_name = get_place_official_name(step.arrival_place_name)
            if official_name is not None:
                step.arrival_place_name = official_name

            official_name = get_place_official_name(step.departure_place_name)
            if official_name is not None:
                step.departure_place_name = official_name


def get_place_official_name(place_name):
    params = open_street_map_url_params.copy()
    params["amenity"] = place_name
    url = open_street_map_url + urllib.parse.urlencode(params)
    res = requests.get(url)
    res.raise_for_status()
    res = res.json()

    if len(res) == 0:
        return None
    else:
        res = res[0]["namedetails"]

        if "official_name" in res:
            return res["official_name"]
        else:
            return res["name"]


@defer.inlineCallbacks
def crawl(crawler_process, result):
    should_c = True
    for route in result.routes:
        for step in route.legs:
            transport_agency_names = [i.name.lower() for i in step.transit_line.transit_agencies]

            if "flixbus" in transport_agency_names and should_c:
                yield crawler_process.crawl(FlixbusSpider,
                                            request=FlixbusRequest(step.departure_place_name,
                                                                   step.arrival_place_name,
                                                                   step.departure_datetime.date())
                                            )

    reactor.stop()


if __name__ == "__main__":
    departure = "University of Southern Denmark, SDU"
    arrival = "ZOB Hamburg"
    departure_datetime = "2023-12-16T22:00:00Z"

    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    result = google_finder.find_routes(departure, arrival, departure_datetime)
    convert_place_names_to_official(result)

    json_result = jsonable_encoder(result)
    json_object = json.dumps(json_result, indent=4, ensure_ascii=False).encode("utf-8")

    with open("result.json", "w") as out:
        out.write(json_object.decode())

    crawler_process = CrawlerProcess(
        get_crawler_process_settings()
    )

    crawl(crawler_process, result)
    reactor.run()

    with open("result.json", "r") as f:
        print(f.read())
