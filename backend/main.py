import datetime
import urllib.parse
import logging
import requests
from scrapy.crawler import CrawlerProcess
from twisted.internet import defer, reactor

from backend.config import get_settings, get_pipeline_crawler_process_settings
from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.json_serializer import write_to_json_file, encode_json
from backend.spiders.implementations.flixbus_spider import FlixbusSpider
from backend.spiders.spider_base import SpiderRequest

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
    for route in result.routes:
        for step in route.legs:
            transport_agency_names = [i.name.lower() for i in step.transit_line.transit_agencies]

            if "flixbus" in transport_agency_names:
                yield crawler_process.crawl(FlixbusSpider,
                                            request=SpiderRequest(step.departure_place_name,
                                                                  step.arrival_place_name,
                                                                  step.departure_datetime.date())
                                            )

    reactor.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    departure = "University of Southern Denmark, SDU"
    arrival = "ZOB Hamburg"
    departure_datetime = datetime.datetime(2023, 12, 16, 16, 30)

    logger.info(f"Searching... ('{departure}', '{arrival}', {departure_datetime})")

    google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    result = google_finder.find_routes(departure, arrival, departure_datetime)
    convert_place_names_to_official(result)
    # result = aux_result # use to skip the previous computations
    json_result = encode_json(result)

    with open("result.json", "w") as out:
        write_to_json_file(out, json_result)

    crawler_process = CrawlerProcess(
        get_pipeline_crawler_process_settings()
    )

    crawl(crawler_process, result)
    reactor.run()

    with open("result.json", "r") as f:
        print(f.read())
