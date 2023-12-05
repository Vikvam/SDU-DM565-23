from google_route_finder import GoogleRouteFinder
from props_reader import PropertiesReader

PROPERTIES_FILE = "../../conf.properties"

start_address = "University of Southern Denmark, SDU"
end_address = "ZOB Hamburg"


def main():
    props_reader = PropertiesReader()
    props = props_reader.load_properties(PROPERTIES_FILE)

    route_finder = GoogleRouteFinder(props["GOOGLE_MAPS_API_KEY"])
    route_finder.find_routes(start_address, end_address)


if __name__ == '__main__':
    main()
