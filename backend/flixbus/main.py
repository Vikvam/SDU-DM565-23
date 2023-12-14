import os
import sys
from time import sleep
from dotenv import load_dotenv
import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from abc import ABC
from dataclasses import dataclass
from datetime import date
from selenium.webdriver.support.wait import WebDriverWait

load_dotenv()

sys.path.append("..")
from selenium_middleware import SeleniumRequest

@dataclass
class FlixbusRequest:
    origin_place_name: str
    destination_place_name: str
    date: date


class FlixbusSpider(scrapy.Spider, ABC):
    name: str = "Flixbus shop spider"
    _BASE_URL = f"https://global.flixbus.com"

    def __init__(self, request: FlixbusRequest, timeout=5, **kwargs):
        super().__init__(**kwargs)
        self.request = request
        self.timeout = timeout

    def start_requests(self) -> [SeleniumRequest]:
        yield SeleniumRequest(
            url=self._BASE_URL,
            callback=self.parse,
            do_before=self.selenium_search,
            wait_until=self.page_loaded
        )

    def selenium_search(self, driver):
        def selenium_accept_cookies(driver):
            def get_shadow_root_parent(driver): return driver.find_element(By.ID, "usercentrics-root")
            WebDriverWait(driver, self.timeout).until(get_shadow_root_parent)
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', get_shadow_root_parent(driver))
            def get_cookie_button(_): return shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-deny-all-button']")
            WebDriverWait(driver, self.timeout).until(get_cookie_button)
            driver.execute_script('return arguments[0].click()', get_cookie_button(driver))

        def selenium_input_search(driver):
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

        def selenium_url_search(driver):
            url = driver.current_url
            print(url)
            url += url.split("&rideDate")[0] + f"&rideDate={self.request.date.strftime('%d.%m.%Y')}&adult=1&_locale=en&features%5Bfeature.enable_distribusion%5D=1&features%5Bfeature.train_cities_only%5D=0&features%5Bfeature.auto_update_disabled%5D=0&features%5Bfeature.webc_search_station_suggestions_enabled%5D=0&features%5Bfeature.darken_page%5D="
            driver.get(url)

        selenium_accept_cookies(driver)
        selenium_input_search(driver)
        selenium_url_search(driver)

    def page_loaded(self, driver):
        return driver.find_element(By.CSS_SELECTOR, "ul.ResultsList__resultsList___eGsLK")

    def parse(self, response: scrapy.http.Response, **kwargs):
        driver = response.request.meta["driver"]
        # WebDriverWait(driver, response.request.wait_timeout).until(self.page_loaded)

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
    process = CrawlerProcess({
        "DOWNLOADER_MIDDLEWARES": {
            "selenium_middleware.SeleniumMiddleware": 800,
        },
        "SELENIUM_DRIVER_NAME": "firefox",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": os.getenv("FIREFOX_PATH_DRIVER"),
        "SELENIUM_DRIVER_ARGUMENTS": ["--headless"],
        "LOG_LEVEL": "WARNING",
    })
    # process.crawl(FlixbusSpider, request=FlixbusRequest("Berlin", "Copenhagen", date(2023, 12, 31)))
    process.crawl(FlixbusSpider, request=FlixbusRequest("Praha", "Mnichov", date(2024, 1, 31)))
    process.start()

    # print(flixbus_scrape("Berlin", 'Copenhagen', '01.12.2023'))

