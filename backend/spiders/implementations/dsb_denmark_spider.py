from datetime import datetime
from time import sleep

from money import Money
from scrapy.http import Response
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from backend.google_api.datetime_converter import convert_datetime_to_time_str, convert_str_to_time, \
    combine_date_with_time
from backend.spiders.selenium_middleware import SeleniumRequest
from backend.spiders.spider_base import BaseSpider, SpiderRequest, SpiderItem


class DsbDenmarkSpider(BaseSpider):
    name = "dsb_europe_spider"
    TRAVEL_AGENCY = "DSB"
    BASE_URL = "https://www.dsb.dk/"
    DEFAULT_CURRENCY = "DKK"

    def __init__(self, request: SpiderRequest, **kwargs):
        super().__init__(self.TRAVEL_AGENCY, request, **kwargs)

    def start_requests(self) -> [SeleniumRequest]:
        yield SeleniumRequest(
            url=self.BASE_URL,
            callback=self.parse,
            do_before=self.accept_cookies,
            wait_until=self.has_base_page_loaded,
            wait_timeout=self._timeout
        )

    def parse(self, response: Response, **kwargs):
        driver = response.request.meta["driver"]

        self._input_insert_text(driver,
                                By.CSS_SELECTOR, 'input[name="criteria[0].DepartLocation.Name"]',
                                self._request.departure_place)
        self._autocomplete_search(driver, By.ID, 'react-autowhatever-DepartLocation--item-0')

        self._input_insert_text(driver,
                                By.CSS_SELECTOR, 'input[name="criteria[0].ArriveLocation.Name"]',
                                self._request.arrival_place)
        self._autocomplete_search(driver, By.ID, 'react-autowhatever-ArriveLocation--item-0')

        self._insert_departure_date(driver)
        self._insert_departure_time(driver)
        self._goto_results_page(driver)

        self._wait_for_results(driver)
        yield from self._parse_results(driver)

    @staticmethod
    def accept_cookies(driver):
        try:
            DsbDenmarkSpider._click_button(driver, By.CLASS_NAME, "coi-banner__accept")
        except WebDriverException:
            pass

    @staticmethod
    def has_base_page_loaded(driver):
        return driver.find_element(By.CLASS_NAME, 'search-box__panel')

    def _autocomplete_search(self, driver, by, identifier):
        WebDriverWait(driver, self._timeout).until(EC.element_to_be_clickable(
            (by, identifier)
        ))
        self._click_button(driver, by, identifier)

    def _insert_departure_date(self, driver):
        maximum_month_traversals = 2

        self._click_button(driver, By.ID, 'SearchDate3')

        for _ in range(maximum_month_traversals):
            try:
                self._click_button(driver, By.CSS_SELECTOR,
                                   f'button[data-pika-year="{self._request.departure_datetime.year}"]'
                                   f'[data-pika-month="{self._request.departure_datetime.month - 1}"]'
                                   f'[data-pika-day="{self._request.departure_datetime.day}"]')
            except NoSuchElementException:
                self._click_button(driver, By.CLASS_NAME, 'pika-next')
                continue
            break

    def _insert_departure_time(self, driver):
        max_time_traversals = 100
        departure_date = self._request.departure_datetime
        departure_date = departure_date.replace(minute=15 * (departure_date.minute // 15))
        departure_time = convert_datetime_to_time_str(departure_date)
        input_css_selector = 'input[name="criteria[0].SearchTime"]'
        self._click_button(driver, By.CSS_SELECTOR, input_css_selector)
        input = driver.find_element(By.CSS_SELECTOR, input_css_selector)

        for _ in range(max_time_traversals):
            input_value = driver.execute_script("return arguments[0].value;", input)

            if input_value == departure_time:
                input.send_keys(Keys.ENTER)
                break
            else:
                input.send_keys(Keys.DOWN)

    @staticmethod
    def _insert_value_to_hidden_input(driver, selector, value):
        driver.execute_script('''
            var selector = arguments[0];
            var value = arguments[1];
            selector.value = value;
        ''', selector, value)

    def _goto_results_page(self, driver):
        self._click_button(driver, By.ID, 'formSubmitBtn')
        WebDriverWait(driver, self._timeout).until(
            EC.presence_of_element_located((By.ID, 'travel-results'))
        )

    @staticmethod
    def _input_insert_text(driver, by, identifier, value):
        input = driver.find_element(by, identifier)
        input.send_keys(value)

    @staticmethod
    def _click_button(driver, by, value):
        button = driver.find_element(by, value)
        button.click()
        sleep(.2)

    @staticmethod
    def _wait_for_results(driver):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'journey'))
        )

    def _parse_results(self, driver):
        journey_containers = driver.find_elements(By.CLASS_NAME, 'journey-container')

        for container in journey_containers:
            item = self._parse_result_item(container)
            print(item)
            yield item

    def _parse_result_item(self, container):
        if self._selector_exists(container, By.CLASS_NAME, 'daybreak-divider'):
            day = container.find_element(By.CLASS_NAME, 'daybreak-divider').text
            day = day.split(' ')[1]
            day = day.rstrip('.')
            self._request.departure_datetime = self._request.departure_datetime.replace(day=int(day))

        departure_datetime, arrival_datetime = self._get_journey_time_from_result(container)
        price = self._get_price_from_result_item(container)

        return SpiderItem(
            self._request.departure_place,
            self._request.arrival_place,
            departure_datetime,
            arrival_datetime,
            price,
            self.TRAVEL_AGENCY
        )

    @staticmethod
    def _selector_exists(driver, by, value):
        try:
            driver.find_element(by, value)
        except NoSuchElementException:
            return False
        return True

    def _get_journey_time_from_result(self, container):
        journey_time = container.find_element(By.CLASS_NAME, 'journey-times__time').text
        journey_time = journey_time.split(" – ")
        journey_departure_datetime = convert_str_to_time(journey_time[0])
        journey_departure_datetime = datetime.combine(self._request.departure_datetime, journey_departure_datetime)
        journey_arrival_datetime = combine_date_with_time(journey_departure_datetime, journey_time[1])
        return journey_departure_datetime, journey_arrival_datetime

    def _get_price_from_result_item(self, container):
        price = container.find_element(By.CLASS_NAME, 'journey-lowestprice__headline').text
        price = price.rstrip(",- ")
        return Money(amount=float(price), currency=self.DEFAULT_CURRENCY)
