from datetime import datetime
from time import sleep

import scrapy
from money import Money
from scrapy import Selector
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from backend.spiders.selenium_middleware import SeleniumRequest
from backend.spiders.spider_base import SpiderRequest, BaseSpider, SpiderItem
from backend.spiders.utils import convert_price_to_money, combine_date_and_time


class FlixbusSpider(BaseSpider):
    name: str = "flixbus_spider"
    _BASE_URL = f"https://global.flixbus.com"
    DEFAULT_CURRENCY = "EUR"

    def __init__(self, request: SpiderRequest, **kwargs):
        super().__init__("flixbus", request, **kwargs)

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
        input_from.send_keys(self._request.departure_place)
        sleep(.5)
        input_from.send_keys([Keys.DOWN, Keys.ENTER])

        input_to = driver.find_element(By.CSS_SELECTOR, "#searchInput-to")
        input_to.clear()
        input_to.send_keys(self._request.arrival_place)
        sleep(.5)
        input_to.send_keys([Keys.DOWN, Keys.ENTER])

        search_button = driver.find_element(By.CSS_SELECTOR, "div[data-e2e='search-button'] > button")
        search_button.click()

    def selenium_url_search(self, driver):
        url = driver.current_url.split("&rideDate")[0]
        url += f"&rideDate={self._request.departure_datetime.strftime('%d.%m.%Y')}&adult=1&_locale=en&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.auto_update_disabled%5D=0&features%5Bfeature.webc_search_station_suggestions_enabled%5D=0&features%5Bfeature.darken_page%5D="
        print(f"Flixbus search: {url}")
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

    def parse_route(self, selector: Selector):
        price_selector = selector.xpath(".//span[contains(@class, 'SearchResult__price___QpySa')]")
        price = "".join(price_selector.xpath(".//text() | .//sup/text()").getall())
        origin_time = selector.xpath(
            ".//div[contains(@class, 'LocationsHorizontal__time___SaJCp')]//span[@aria-hidden='true']/text()").getall()
        origin_time = origin_time[0]
        destination_time = origin_time[1]
        departure_place, arrival_place = selector.xpath(
            ".//div[contains(@class, 'LocationsHorizontal__station___ItGEv')]/span[@aria-hidden='true']/text()").getall()
        print(price, departure_place, arrival_place, origin_time, destination_time)
        return SpiderItem(
            departure_place,
            arrival_place,
            combine_date_and_time(self._request.departure_datetime, origin_time),
            combine_date_and_time(self._request.departure_datetime, destination_time),
            convert_price_to_money(price, self.DEFAULT_CURRENCY),
            self._travel_agency
        )
