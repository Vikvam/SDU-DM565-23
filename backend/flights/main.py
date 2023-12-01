import os
import requests
from dotenv import load_dotenv
from datetime import date
from dataclasses import asdict, dataclass, field
from enum import Enum, StrEnum

load_dotenv()
API_KEY = os.getenv("SKYSCANNER-API-KEY")


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


class SkyscannerAPI:

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
        print(response_json)
        # TODO: handle results

    def get(self, request: SkyscannerRequest):
        self.create_session(request)
        self.await_session()


if __name__ == "__main__":
    api = SkyscannerAPI(API_KEY)
    request = SkyscannerRequest(query_legs=[QueryLeg("CPH", "BER", date(2023, 12, 1))])
    api.get(request)

