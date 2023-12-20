import datetime
from dataclasses import asdict, dataclass, field
from datetime import date

import requests
from money import Money
from strenum import StrEnum

from backend.google_api.google_route_objects import RouteLegTransitAgency, RouteLegTransitLine, RoutePlaceDetails, \
    RouteLeg


class CabinClass(StrEnum):
    CABIN_CLASS_UNSPECIFIED = "CABIN_CLASS_UNSPECIFIED"
    CABIN_CLASS_ECONOMY = "CABIN_CLASS_ECONOMY"
    CABIN_CLASS_PREMIUM_ECONOMY = "CABIN_CLASS_PREMIUM_ECONOMY"
    CABIN_CLASS_BUSINESS = "CABIN_CLASS_BUSINESS"
    CABIN_CLASS_FIRST = "CABIN_CLASS_FIRST"


@dataclass
class QueryLeg:
    origin_place_id: str
    destination_place_id: str
    date: date

    def asdict(self):
        return {
            "originPlaceId": {"iata": self.origin_place_id},
            "destinationPlaceId": {"iata": self.destination_place_id},
            "date": {"year": self.date.year, "month": self.date.month, "day": self.date.day}
        }


@dataclass
class SkyscannerRequest:
    query_legs: [QueryLeg]
    market: str = "DK"
    locale: str = "da-DK"
    currency: str = "DKK"
    cabin_class: CabinClass = CabinClass.CABIN_CLASS_ECONOMY
    adults: int = 1
    children_ages: [int] = field(default_factory=list)

    def asdict(self):
        dict = asdict(self)
        dict.pop("query_legs")
        dict["queryLegs"] = [i.asdict() for i in self.query_legs]
        dict.pop("cabin_class")
        dict["cabinClass"] = self.cabin_class
        return dict


class SkyscannerFlightFinder:
    _BASE_URL = 'https://partners.api.skyscanner.net/apiservices/v3/flights/live/search'

    def __init__(self, api_key: str):
        self.__api_key: str = api_key
        self.session_token: str | None = None
        self.content: dict | None = None

    def create_session(self, request: SkyscannerRequest):
        response = requests.post(
            f"{self._BASE_URL}/create",
            headers={"x-api-key": self.__api_key},
            json={"query": request.asdict()}
        )
        if response.status_code != 200:
            raise RuntimeError(f"Skyscanner session could not be created: {response.status_code}")
        self.session_token = response.json()["sessionToken"]

    def poll_session(self) -> requests.Response:
        if self.session_token is None:
            raise AssertionError("session_token is None, create a session before calling 'poll'")
        response = requests.post(
            f"{self._BASE_URL}/poll/{self.session_token}",
            headers={"x-api-key": self.__api_key}
        )
        return response

    def await_session(self):
        response = self.poll_session()
        while response.json()["status"] == "RESULT_STATUS_INCOMPLETE":
            # TODO?: perhaps should wait for all results > itineraries > id > pricingOptions > price > status ?
            response = self.poll_session()
        if response.json()["status"] != "RESULT_STATUS_COMPLETE":
            raise RuntimeError(f"Skyscanner session could not be evaluated: {response.status_code}")

        response_json = response.json()
        return self._process_request(response_json)

    def _process_request(self, response: dict) -> RouteLeg:
        best_option_id = response['content']['sortingOptions']['best'][0]['itineraryId']
        response_options = response['content']['results']['itineraries']
        best_option = self._find_value_by_key_in_dict_of_dicts(response_options, best_option_id)

        best_option_leg_id = best_option['legIds'][0]
        response_legs = response['content']['results']['legs']
        best_option_leg = self._find_value_by_key_in_dict_of_dicts(response_legs, best_option_leg_id)

        if len(best_option_leg['segmentIds']) > 1:
            raise Exception("Unable to find a direct flight")

        best_option_segment_id = best_option_leg['segmentIds'][0]
        response_segments = response['content']['results']['segments']
        best_option_segment = self._find_value_by_key_in_dict_of_dicts(response_segments, best_option_segment_id)

        departure_airport, arrival_airport = self._get_journey_waypoints(response, best_option_segment)
        departure_airport = RoutePlaceDetails(departure_airport, "", "")
        arrival_airport = RoutePlaceDetails(arrival_airport, "", "")

        departure_datetime, arrival_datetime = self._get_journey_timestamps(best_option_segment)
        lowest_pricing_option = self._find_lowest_pricing_option(best_option['pricingOptions'])

        lowest_price = self._get_lowest_price(lowest_pricing_option)
        transit_agency = self._get_transit_agency(response, lowest_pricing_option)
        transit_line = self._get_transit_line(response, best_option_segment, transit_agency)

        return RouteLeg(departure_airport,
                        arrival_airport,
                        departure_datetime,
                        arrival_datetime,
                        transit_line,
                        lowest_price)

    def _get_journey_waypoints(self, response: dict, best_option_segment: dict) -> (str, str):
        departure_airport_id = best_option_segment['originPlaceId']
        arrival_airport_id = best_option_segment['destinationPlaceId']
        departure_airport = self._get_airport_name(response, departure_airport_id)
        arrival_airport = self._get_airport_name(response, arrival_airport_id)
        return departure_airport, arrival_airport

    def _get_airport_name(self, response: dict, airport_id: str) -> str:
        response_places = response['content']['results']['places']
        airport = self._find_value_by_key_in_dict_of_dicts(response_places, airport_id)
        return airport['name'] + ' Airport ' + f'({airport["iata"]})'

    def _get_journey_timestamps(self, best_option_segment: dict) -> (datetime, datetime):
        departure_datetime = best_option_segment['departureDateTime']
        arrival_datetime = best_option_segment['arrivalDateTime']
        departure_datetime = self._convert_dict_to_datetime(departure_datetime)
        arrival_datetime = self._convert_dict_to_datetime(arrival_datetime)
        return departure_datetime, arrival_datetime

    @staticmethod
    def _get_lowest_price(lowest_pricing_option: dict) -> Money:
        amount = float(int(lowest_pricing_option['price']['amount']) / 1000)
        amount = round(amount, 2)
        return Money(amount=amount, currency="DKK")

    def _get_transit_agency(self, response: dict, lowest_pricing_option: dict) -> RouteLegTransitAgency:
        response_agents = response['content']['results']['agents']
        agent_id = lowest_pricing_option['agentIds'][0]
        agent = self._find_value_by_key_in_dict_of_dicts(response_agents, agent_id)
        return RouteLegTransitAgency(agent['name'], '')

    def _get_transit_line(self, response: dict,
                          best_option_segment: dict,
                          transit_agency: RouteLegTransitAgency
                          ) -> RouteLegTransitLine:
        response_carriers = response['content']['results']['carriers']
        marketing_carrier_id = best_option_segment['marketingCarrierId']
        carrier = self._find_value_by_key_in_dict_of_dicts(response_carriers, marketing_carrier_id)
        carrier_display_code = carrier['displayCode']
        line_number = carrier_display_code + best_option_segment['marketingFlightNumber']
        return RouteLegTransitLine(line_number, "AIR_PLANE", [transit_agency])

    @staticmethod
    def _find_value_by_key_in_dict_of_dicts(data: dict[dict], search_key: str) -> dict | None:
        for key, value in data.items():
            if key == search_key:
                return value

        return None

    @staticmethod
    def _find_lowest_pricing_option(pricing_options: dict) -> dict | None:
        lowest_price = 9_999_999_999
        lowest_pricing_option = None

        for pricing_option in pricing_options:
            price = int(pricing_option['price']['amount'])

            if lowest_price > price:
                lowest_price = price
                lowest_pricing_option = pricing_option

        return lowest_pricing_option

    @staticmethod
    def _convert_dict_to_datetime(data: dict) -> datetime:
        return datetime.datetime(year=data['year'],
                                 month=data['month'],
                                 day=data['day'],
                                 hour=data['hour'],
                                 minute=data['minute'])

    def get(self, request: SkyscannerRequest):
        self.create_session(request)
        return self.await_session()
