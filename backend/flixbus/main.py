import os
from dotenv import load_dotenv
import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from selenium.webdriver.common.by import By
from abc import ABC
from dataclasses import dataclass
from datetime import date

from selenium_middleware import SeleniumRequest


load_dotenv()


@dataclass
class FlixbusRequest:
    origin_place_name: str
    destination_place_name: str
    date: date


class FlixbusSpider(scrapy.Spider, ABC):
    name: str = "Flixbus shop spider"

    @staticmethod
    def _BASE_URL(request: FlixbusRequest):
        return f"https://shop.global.flixbus.com/search?departureCity=40d8f682-8646-11e6-9066-549f350fcb0c&arrivalCity=40de7db1-8646-11e6-9066-549f350fcb0c&route={request.origin_place_name}-{request.destination_place_name}&rideDate={request.date.strftime('%d.%m.%Y')}&adult=1&_locale=en&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.auto_update_disabled%5D=0&features%5Bfeature.webc_search_station_suggestions_enabled%5D=0&features%5Bfeature.darken_page%5D="

    def __init__(self, request: FlixbusRequest, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    def start_requests(self) -> [SeleniumRequest]:
        yield SeleniumRequest(url=self._BASE_URL(self.request), callback=self.parse, wait_until=self.page_loaded)

    def page_loaded(self, driver):
        print("!!!", driver.find_element(By.CSS_SELECTOR, "ul.ResultsList__resultsList___eGsLK"))
        return driver.find_element(By.CSS_SELECTOR, "ul.ResultsList__resultsList___eGsLK")

    def parse(self, response: scrapy.http.Response, **kwargs):
        def parse_route(selector):
            price_selector = selector.xpath(".//span[contains(@class, 'SearchResult__price___QpySa')]")
            price = "".join(price_selector.xpath(".//text() | .//sup/text()").getall())
            origin_destination_time = selector.xpath(".//div[contains(@class, 'LocationsHorizontal__time___SaJCp')]//span[@aria-hidden='true']/text()").getall()
            origin_time = origin_destination_time[0]
            destination_time = origin_destination_time[1]
            origin_place_name, destination_place_name = selector.xpath(".//div[contains(@class, 'LocationsHorizontal__station___ItGEv')]/span[@aria-hidden='true']/text()").getall()
            print(price, origin_place_name, destination_place_name, origin_time, destination_time)

        routes_selector: [Selector] = response.xpath("//ul[contains(@class, 'ResultsList__resultsList___eGsLK')]/li//div[contains(@class, 'SearchResult__rowRideAndPrice___u0TJA')]")
        for route_selector in routes_selector:
            parse_route(route_selector)


if __name__ == "__main__":
    request = FlixbusRequest("Berlin", "Copenhagen", date(2023, 12, 1))
    process = CrawlerProcess({
        "DOWNLOADER_MIDDLEWARES": {
            "selenium_middleware.SeleniumMiddleware": 800,
        },
        "SELENIUM_DRIVER_NAME": "firefox",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": os.getenv("FIREFOX_PATH_DRIVER"),
        "SELENIUM_DRIVER_ARGUMENTS": ["--headless"],
        "LOG_LEVEL": "WARNING",
    })
    process.crawl(FlixbusSpider, request=request)
    process.start()

    # print(flixbus_scrape("Berlin", 'Copenhagen', '01.12.2023'))

