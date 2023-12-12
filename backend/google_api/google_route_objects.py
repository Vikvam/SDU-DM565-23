from dataclasses import dataclass
from datetime import datetime
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
class RouteLeg:
    departure_place_name: str
    arrival_place_name: str
    departure_datetime: datetime
    arrival_datatime: datetime
    transit_line: RouteLegTransitLine
    price: Money = None


@dataclass
class Route:
    legs: List[RouteLeg]


@dataclass
class ResponseBody:
    origin_address: str
    destination_address: str
    routes: List[Route]
