from dataclasses import dataclass
from enum import Enum, auto
from typing import List


@dataclass
class Location:
    latitude: int
    longitude: int


@dataclass
class TransitStop:
    name: str
    location: Location


@dataclass
class TransitStopDetails:
    arrivalStop: List[TransitStop]
    arrivalTime: str
    departureStop: TransitStop
    departureTime: str


@dataclass
class LocalizedText:
    text: str
    languageCode: str


@dataclass
class LocalizedTime:
    time: LocalizedText
    timeZone: str


@dataclass
class TransitDetailsLocalizedValues:
    arrivalTime: LocalizedTime
    departureTime: LocalizedTime


@dataclass
class TransitAgency:
    name: str
    phoneNumber: str
    uri: str


class TransitVehicleType(Enum):
    TRANSIT_VEHICLE_TYPE_UNSPECIFIED = auto()
    BUS = auto()
    CABLE_CAR = auto()
    COMMUTER_TRAIN = auto()
    FERRY = auto()
    FUNICULAR = auto()
    GONDOLA_LIFT = auto()
    HEAVY_RAIL = auto()
    HIGH_SPEED_TRAIN = auto()
    INTERCITY_BUS = auto()
    LONG_DISTANCE_TRAIN = auto()
    METRO_RAIL = auto()
    MONORAIL = auto()
    RAIL = auto()
    SHARE_TAXI = auto()
    SUBWAY = auto()
    TRAM = auto()
    TROLLEYBUS = auto()


@dataclass
class TransitVehicle:
    name: LocalizedText
    type: TransitVehicleType
    iconUri: str
    localIconUri: str


@dataclass
class TransitLine:
    agencies: List[TransitAgency]
    name: str
    uri: str
    color: str
    iconUri: str
    nameShort: str
    textColor: str
    vehicle: TransitVehicle


@dataclass
class RouteLegStepTransitDetails:
    stopDetails: TransitStopDetails
    localizedValues: TransitDetailsLocalizedValues
    headsing: str
    headway: str
    transitLine: TransitLine
    stopCount: int
    tripShortText: str


@dataclass
class RouteLegStep:
    transitDetails: RouteLegStepTransitDetails


@dataclass
class RouteLeg:
    steps: List[RouteLegStep]


@dataclass
class Route:
    legs: List[RouteLeg]


@dataclass
class ResponseBody:
    routes: List[Route]
