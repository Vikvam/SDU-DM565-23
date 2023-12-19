from datetime import datetime

from backend.config import get_settings
from google_route_finder import GoogleRouteFinder

start_address = "University of Southern Denmark, SDU"
end_address = "ZOB Hamburg"


def main():
    route_finder = GoogleRouteFinder(get_settings().google_maps_api_key)
    result = route_finder.find_routes(start_address, end_address, datetime.now())
    print_routes(result.routes)


def print_routes(routes):
    for i, route in enumerate(routes):
        print(f"Route #{i + 1}:")

        for j, step in enumerate(route.legs):
            print(f" -> Step #{j + 1}: start: {step.departure}, end: {step.arrival}, "
                  f"line: {step.transit_line.line_name}, provider: {step.transit_line.transit_agencies[0].name}")


if __name__ == '__main__':
    main()
