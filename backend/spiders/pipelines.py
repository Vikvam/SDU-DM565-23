import json

from backend.google_api.datetime_converter import convert_str_to_datetime
from backend.json_serializer import write_to_json_file


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

                if transit_agency_name == item.transport_agent_name.lower():
                    departure_datetime = convert_str_to_datetime(step['departure_datetime'])
                    arrival_datetime = convert_str_to_datetime(step['arrival_datetime'])


                    if (departure_datetime.time() == item.departure_datetime.time() and
                            arrival_datetime.time() == item.arrival_date_time.time()):
                        step['price'] = {
                            "amount": "{:.2f}".format(item.price.amount),
                            "currency:": item.price.currency
                        }

    def close_spider(self, spider):
        self.erase_file_content(self._file)
        write_to_json_file(self._file, self._result)
        self._file.close()

    @staticmethod
    def erase_file_content(file):
        file.seek(0)
        file.truncate(0)
