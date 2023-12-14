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
from selenium.webdriver.support import expected_conditions as EC

sys.path.append("..")
from selenium_middleware import SeleniumRequest

load_dotenv()
load_dotenv("../.env")


@dataclass
class DBRequest:
    from_name: str
    to_name: str
    date: date


class DBSpider(scrapy.Spider, ABC):
    name: str = "DB shop spider"
    _BASE_URL = "https://www.bahn.de/"

    def __init__(self, request: DBRequest, timeout=5, **kwargs):
        super().__init__(**kwargs)
        self.request = request
        self.timeout = timeout

    def start_requests(self) -> [SeleniumRequest]:
        yield SeleniumRequest(
            url=self._BASE_URL,
            callback=self.parse,
            do_before=self.selenium_search,
            wait_until=self.page_loaded,
            wait_timeout=self.timeout
        )
        # yield SeleniumRequest(
        #     url="https://www.bahn.de/buchung/fahrplan/suche#sts=true&so=Berlin%20Hbf&zo=Hamburg%20Hbf&kl=2&r=13:16:KLASSENLOS:1&soid=A%3D1%40O%3DBerlin%20Hbf%40X%3D13369549%40Y%3D52525589%40U%3D81%40L%3D8011160%40B%3D1%40p%3D1702322185%40&zoid=A%3D1%40O%3DHamburg%20Hbf%40X%3D10006909%40Y%3D53552733%40U%3D81%40L%3D8002549%40B%3D1%40p%3D1702322185%40&sot=ST&zot=ST&soei=8011160&zoei=8002549&hd=2023-12-31",
        #     callback=self.parse,
        #     wait_until=self.page_loaded,
        #     wait_timeout=self.timeout
        # )

    def selenium_search(self, driver):
        def selenium_accept_cookies(driver):
            def get_shadow_root(driver): return driver.execute_script('return arguments[0].shadowRoot', driver.find_element(By.CSS_SELECTOR, "body > div"))
            WebDriverWait(driver, self.timeout).until(get_shadow_root)
            shadow_root = get_shadow_root(driver)

            def get_cookie_button(_): return shadow_root.find_element(By.CSS_SELECTOR, "button.js-accept-essential-cookies")
            WebDriverWait(driver, self.timeout).until(get_cookie_button)
            get_cookie_button(driver).click()
            sleep(.2)

        def selenium_input_search(driver):
            WebDriverWait(driver, self.timeout).until(lambda driver: driver.find_element(By.CSS_SELECTOR, "form.quick-finder__form"))
            input_from = driver.find_element(By.CSS_SELECTOR, ".quick-finder-basic__stations > div:nth-child(1) > div > input")
            input_to = driver.find_element(By.CSS_SELECTOR, ".quick-finder-basic__stations > div:nth-child(3) > div > input")

            def is_stop_autocomplete_on(driver):
                return driver.find_element(By.CLASS_NAME, "db-web-autocomplete__menu-overlay").size["height"] > 0

            for inp, val in ((input_from, self.request.from_name), (input_to, self.request.to_name)):
                inp.clear()
                inp.send_keys(val)
                WebDriverWait(driver, self.timeout).until(is_stop_autocomplete_on)
                inp.send_keys([Keys.DOWN, Keys.ENTER])

            WebDriverWait(driver, self.timeout).until(lambda driver: not is_stop_autocomplete_on(driver))
            search_button = WebDriverWait(driver, self.timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".quick-finder-basic > button:last-of-type")))
            while driver.current_url == self._BASE_URL:
                search_button.click()

        def selenium_url_search(driver):
            url = driver.current_url
            url = url.split("&hd=")[0] + f"&hd={self.request.date.strftime('%Y-%m-%d')}"
            driver.get(url)
            print(f"DB search: {url}")

        try: selenium_accept_cookies(driver)
        except TimeoutException: pass
        selenium_input_search(driver)
        WebDriverWait(driver, self.timeout).until(self.page_loaded)
        selenium_url_search(driver)

    def page_loaded(self, driver):
        return driver.find_element(By.CSS_SELECTOR, "div.loading-indicator ul li")

    def parse(self, response: scrapy.http.Response, **kwargs):
        def parse_route(selector):
            price = selector.xpath(".//span[contains(@class, 'reise-preis__preis')]/text()").get()
            origin_time = selector.xpath(".//time[contains(@class, 'reiseplan__uebersicht-uhrzeit-sollzeit')]/text()").get()
            destination_time = "TODO"
            from_name = selector.xpath(".//span[contains(@class, 'test-reise-beschreibung-start-value')]/text()").get()
            to_name = selector.xpath(".//span[contains(@class, 'test-reise-beschreibung-ziel-value')]/text()").get()
            print(price, from_name, to_name, origin_time, destination_time)

        routes_selector: [Selector] = response.css("ul.verbindung-list li")
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
    process.crawl(DBSpider, request=DBRequest("Berlin Hb", "Hamburg Hb", date(2023, 12, 31)))
    process.start()

    # print(flixbus_scrape("Berlin", 'Copenhagen', '01.12.2023'))

