from datetime import datetime

from google_route_finder import GoogleRouteFinder
from props_reader import PropertiesReader

PROPERTIES_FILE = "../../conf.properties"

start_address = "University of Southern Denmark, SDU"
end_address = "ZOB Hamburg"


def main():
    props_reader = PropertiesReader()
    props = props_reader.load_properties(PROPERTIES_FILE)

    route_finder = GoogleRouteFinder(props["GOOGLE_MAPS_API_KEY"])
    result = route_finder.find_routes(start_address, end_address, datetime.now())
    print_routes(result.routes)


def print_routes(routes):
    for i, route in enumerate(routes):
        print(f"Route #{i + 1}:")

        for j, step in enumerate(route.legs):
            print(
                f" -> Step #{j + 1}: start: {step.departure_place_name}, end: {step.arrival_place_name}, "
                f"line: {step.transit_line.line_name}, provider: {step.transit_line.transit_agencies[0].name}")


if __name__ == '__main__':
    main()
