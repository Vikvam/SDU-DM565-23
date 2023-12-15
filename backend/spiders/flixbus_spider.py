from abc import ABC
from time import sleep

import scrapy
from attr import dataclass
from money import Money
from scrapy import Selector
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import date, datetime

from backend.spiders.selenium_middleware import SeleniumRequest
from backend.spiders.spider_item import SpiderItem


@dataclass
class FlixbusRequest:
    origin_place_name: str
    destination_place_name: str
    date: date


class FlixbusSpider(scrapy.Spider, ABC):
    name: str = "Flixbus shop spider"
    transport_agency = "flixbus"
    _BASE_URL = f"https://global.flixbus.com"

    def __init__(self, request: FlixbusRequest, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    def start_requests(self) -> [SeleniumRequest]:
        yield SeleniumRequest(
            url=self._BASE_URL,
            callback=self.parse,
            do_before=self.selenium_search,
            wait_until=self.page_loaded
        )

    def selenium_accept_cookies(self, driver):
        WebDriverWait(driver, 5).until(lambda driver: driver.find_element(By.ID, "usercentrics-root"))
        shadow_root = driver.execute_script('return arguments[0].shadowRoot',
                                            driver.find_element(By.ID, "usercentrics-root"))
        WebDriverWait(driver, 5).until(lambda driver: shadow_root.find_element(By.CSS_SELECTOR, "button.bqSTzv"))
        driver.execute_script('return arguments[0].click()', shadow_root.find_element(By.CSS_SELECTOR, "button.bqSTzv"))

    def selenium_input_search(self, driver):
        input_from = driver.find_element(By.CSS_SELECTOR, "#searchInput-from")
        input_from.clear()
        input_from.send_keys(self.request.origin_place_name)
        sleep(.5)
        input_from.send_keys([Keys.DOWN, Keys.ENTER])

        input_to = driver.find_element(By.CSS_SELECTOR, "#searchInput-to")
        input_to.clear()
        input_to.send_keys(self.request.destination_place_name)
        sleep(.5)
        input_to.send_keys([Keys.DOWN, Keys.ENTER])

        search_button = driver.find_element(By.CSS_SELECTOR, "div[data-e2e='search-button'] > button")
        search_button.click()

    def selenium_url_search(self, driver):
        url = driver.current_url.split("&rideDate")[0]
        url += f"&rideDate={self.request.date.strftime('%d.%m.%Y')}&adult=1&_locale=en&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.auto_update_disabled%5D=0&features%5Bfeature.webc_search_station_suggestions_enabled%5D=0&features%5Bfeature.darken_page%5D="
        print(url)
        driver.get(url)

    def selenium_search(self, driver):
        self.selenium_accept_cookies(driver)
        self.selenium_input_search(driver)
        self.selenium_url_search(driver)

    def page_loaded(self, driver):
        return driver.find_element(By.CSS_SELECTOR, "ul.ResultsList__resultsList___eGsLK")

    def parse(self, response: scrapy.http.Response, **kwargs):
        driver = response.request.meta["driver"]
        WebDriverWait(driver, response.request.wait_timeout).until(self.page_loaded)
        routes_selector: [Selector] = response.xpath(
            "//ul[contains(@class, 'ResultsList__resultsList___eGsLK')]/li//div[contains(@class, 'SearchResult__rowRideAndPrice___u0TJA')]")

        for route_selector in routes_selector:
            yield self.parse_route(route_selector)

    def parse_route(self, selector):
        price_selector = selector.xpath(".//span[contains(@class, 'SearchResult__price___QpySa')]")
        price = "".join(price_selector.xpath(".//text() | .//sup/text()").getall())
        origin_destination_time = selector.xpath(
            ".//div[contains(@class, 'LocationsHorizontal__time___SaJCp')]//span[@aria-hidden='true']/text()").getall()
        origin_time = origin_destination_time[0]
        destination_time = origin_destination_time[1]
        origin_place_name, destination_place_name = selector.xpath(
            ".//div[contains(@class, 'LocationsHorizontal__station___ItGEv')]/span[@aria-hidden='true']/text()").getall()
        print(price, origin_place_name, destination_place_name, origin_time, destination_time)

        return SpiderItem(
            origin_place_name,
            destination_place_name,
            datetime.combine(self.request.date, datetime.strptime(origin_time, "%H:%M").time()),
            datetime.combine(self.request.date, datetime.strptime(destination_time, "%H:%M").time()),
            Money(amount=float(price[1:]), currency="EUR"),  # ASSUMING EUR AS CURRENCY
            self.transport_agency
        )
