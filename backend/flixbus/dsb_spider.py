from dataclasses import dataclass

import scrapy
from scrapy import Item, Field, signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@dataclass
class DsbSpiderRequest:
    place_name: str


class DsbSpiderResponse(Item):
    place_code = Field()


class DsbSpider(scrapy.Spider):
    name = "dsb_spider"
    custom_settings = {
        "USER_AGENT": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    }
    base_url = "https://travel.b-europe.com/dsb-rail/en/booking"

    def __init__(self, request, **kwargs):
        super().__init__(**kwargs)
        self._request = request

    def start_requests(self):
        yield SeleniumRequest(url=self.base_url,
                              callback=self.parse_result,
                              wait_until=self.has_page_loaded,
                              wait_time=10)

    def has_page_loaded(self, driver):
        return driver.find_element(By.ID, 'departure-station')

    def parse_result(self, response):
        driver = response.request.meta["driver"]

        self.accept_cookies(driver)
        search_input = driver.find_element(By.ID, "departure-station")
        item = DsbSpiderResponse()
        item['place_code'] = self.get_place_code(driver, search_input, self._request.place_name)
        yield item

    def accept_cookies(self, driver):
        accept_cookies_btn = driver.find_element(By.CLASS_NAME, "coi-banner__accept")
        accept_cookies_btn.click()

    def get_place_code(self, driver, form_input, value):
        wait = WebDriverWait(driver, 5)

        form_input.clear()
        wait.until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, 'div[data-index="0"]')
        ))

        form_input.send_keys(value)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div[data-index="0"]')
        ))
        first_proposition = driver.find_element(By.CSS_SELECTOR, 'div[data-index="0"]')
        first_proposition.click()

        return form_input.get_attribute("data-station-rcode")


def get_dsb_place_code(place_name):
    _item = None

    def set_item(item):
        nonlocal _item
        _item = item['place_code']

    dispatcher.connect(set_item, signal=signals.item_scraped)
    request = DsbSpiderRequest(place_name)
    process = CrawlerProcess({
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_selenium.SeleniumMiddleware': 800,
        },
        "SELENIUM_DRIVER_NAME": "chrome",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": None,
        "SELENIUM_DRIVER_ARGUMENTS": [],
        "LOG_LEVEL": "WARNING",
    })

    process.crawl(DsbSpider, request=request)
    process.start()
    return _item


print(get_dsb_place_code('Berlin Hbf'))