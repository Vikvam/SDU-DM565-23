from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import List

from money import Money


@dataclass
class RouteLegTransitAgency:
    name: str
    uri: str


@dataclass
class RouteLegTransitLine:
    line_name: str
    vehicle_type: str
    transit_agencies: list[RouteLegTransitAgency]


@dataclass
class RoutePlaceDetails:
    name: str
    longitude: str
    latitude: str


@dataclass
class RouteLeg:
    departure: RoutePlaceDetails
    arrival: RoutePlaceDetails
    departure_datetime: datetime
    arrival_datetime: datetime
    transit_line: RouteLegTransitLine
    price: Money = None


@dataclass
class Route:
    legs: List[RouteLeg]


class GoogleDatetimeOption(Enum):
    DEPARTURE_TIME = auto()
    ARRIVAL_TIME = auto

@dataclass
class ResponseBody:
    origin_address: str
    destination_address: str
    journey_datetime: datetime
    journey_datetime_option: GoogleDatetimeOption
    routes: List[Route]
