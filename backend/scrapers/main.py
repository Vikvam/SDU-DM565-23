from dsb_scraper import DsbScraper
import constants as const


def main():
    departure = 'Odense St'
    arrival = 'København H'

    with DsbScraper(const.CHROME_DRIVER_PATH) as scaper:
        routes = scaper.find_routes(departure, arrival)
        print_routes(routes)


def print_routes(routes):
    for i, route in enumerate(routes):
        cost = '---' if route.cost is None else route.cost

        print("Option #{} line: {} time: {} cost: {}"
              .format(i, route.line_name, route.time, cost))


if __name__ == '__main__':
    main()
