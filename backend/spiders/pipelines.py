import json
from datetime import datetime

from backend.google_api.google_route_finder import GoogleRouteFinder


class RoutePipeline:
    def __init__(self):
        self._file = None
        self._result = {}

    def open_spider(self, spider):
        self._file = open("result.json", "r+")
        self._result = json.load(self._file)

    def process_item(self, item, spider):
        for route in self._result['routes']:
            for step in route['legs']:
                transit_agency_name = step['transit_line']['transit_agencies'][0]['name'].lower()

                if transit_agency_name == item.transport_agent_name:
                    departure_datetime = datetime.strptime(step['departure_datetime'],
                                                           "%Y-%m-%dT%H:%M:%S")
                    arrival_datetime = datetime.strptime(step['arrival_datetime'],
                                                         "%Y-%m-%dT%H:%M:%S")

                    if departure_datetime.time() == item.departure_datetime.time() and arrival_datetime.time() == item.arrival_date_time.time():
                        step['price'] = {
                            "amount": "{:.2f}".format(item.price.amount),
                            "currency:": item.price.currency
                        }

    def close_spider(self, spider):
        json_to_write = json.dumps(self._result, indent=4)
        self._file.seek(0)
        self._file.truncate(0)
        self._file.write(json_to_write + "\n")
        self._file.close()
