from datetime import datetime
from time import sleep

from money import Money
from scrapy.http import Response
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from backend.google_api.datetime_converter import combine_date_with_time, convert_datetime_to_str, convert_str_to_time
from backend.spiders.selenium_middleware import SeleniumRequest
from backend.spiders.spider_base import BaseSpider, SpiderRequest, SpiderItem
from selenium.webdriver.support import expected_conditions as EC


class DsbEuropeSpider(BaseSpider):
    name = "dsb_europe_spider"
    TRAVEL_AGENCY = "DSB"
    BASE_URL = "https://travel.b-europe.com/dsb-rail/en/booking#TravelWish"
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

    @staticmethod
    def accept_cookies(driver):
        accept_cookies_btn = driver.find_element(By.CLASS_NAME, "coi-banner__accept")
        accept_cookies_btn.click()

    @staticmethod
    def has_base_page_loaded(driver):
        return driver.find_element(By.CLASS_NAME, "coi-banner__summary")

    def parse(self, response: Response, **kwargs):
        driver = response.request.meta["driver"]

        self._insert_place_name(driver, 'departure-station', self._request.departure_place)
        self._insert_place_name(driver, 'return-station', self._request.arrival_place)

        self._change_trip_to_one_way(driver)
        self._insert_departure_time(driver)
        sleep(.4)
        self._insert_departure_date(driver)

        sleep(.4)
        self._click_search_routes_button(driver)
        self._wait_for_search_results(driver)
        yield from self._process_result(driver)

    def _insert_place_name(self, driver, input_id, value):
        input = driver.find_element(By.ID, input_id)
        input.send_keys(value)
        sleep(.3)
        input.send_keys(Keys.ENTER)

        WebDriverWait(driver, self._timeout).until(
            EC.invisibility_of_element((By.CLASS_NAME, 'autocomplete-suggestions'))
        )

    def _change_trip_to_one_way(self, driver):
        self._click_button(driver, By.CSS_SELECTOR, ".selectorTravelType > label:nth-child(2)")

    def _insert_departure_time(self, driver):
        hour_checkboxes = [
            {"id": 5, "from": 4, "to": 6}, {"id": 7, "from": 6, "to": 8}, {"id": 9, "from": 8, "to": 10},
            {"id": 11, "from": 10, "to": 12}, {"id": 13, "from": 12, "to": 14}, {"id": 15, "from": 14, "to": 16},
            {"id": 17, "from": 16, "to": 18}, {"id": 19, "from": 18, "to": 20}, {"id": 21, "from": 20, "to": 4}
        ]
        min_hour_value = hour_checkboxes[0]["from"]
        departure_hour = self._request.departure_datetime.hour
        checkbox_id = hour_checkboxes[-1]["id"]

        if departure_hour >= min_hour_value:
            for checkbox in hour_checkboxes:
                if checkbox['from'] <= departure_hour < checkbox['to']:
                    checkbox_id = checkbox['id']
                    break

        self._click_button(driver, By.ID, "departure-time")
        self._click_button(driver, By.CSS_SELECTOR, f'label[data-travel-time="{checkbox_id}"]')

    def _insert_departure_date(self, driver):
        self._click_button(driver, By.ID, "departure-date")

        calendars = driver.find_elements(By.CLASS_NAME, "pika-lendar")

        for calendar in calendars:
            calendar_year_month = self._get_calendar_year_and_month(driver, calendar)
            departure_month_year = self._request.departure_datetime.strftime("%B %Y")

            if calendar_year_month == departure_month_year:
                button_name = f"button[data-pika-day='{self._request.departure_datetime.day}']"
                self._wait_for_calendar_button_to_be_clickable(driver, button_name)
                self._click_button(driver, By.CSS_SELECTOR, button_name)
                break

        self._wait_for_calendar_vanishing(driver)

    @staticmethod
    def _get_calendar_year_and_month(driver, calendar):
        calendar_content = calendar.find_elements(By.CLASS_NAME, "pika-label")
        month_name = DsbEuropeSpider._get_text_content_without_nested_selectors_content(driver, calendar_content[0])
        year = calendar_content[1].text
        return month_name + " " + year

    @staticmethod
    def _get_text_content_without_nested_selectors_content(driver, selector):
        return driver.execute_script("return arguments[0].firstChild.textContent;", selector).strip()

    def _wait_for_calendar_vanishing(self, driver):
        WebDriverWait(driver, self._timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'pika-single'))
        )

    def _wait_for_calendar_button_to_be_clickable(self, driver, button_name):
        WebDriverWait(driver, self._timeout).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, button_name))
        )

    @staticmethod
    def _click_search_routes_button(driver):
        DsbEuropeSpider._click_button(driver, By.ID, "ShowOutboundActionId")

    def _wait_for_search_results(self, driver):
        WebDriverWait(driver, self._timeout).until(
            EC.presence_of_element_located((By.ID, "OutboundTrainSelectionZone")))

    def _process_result(self, driver):
        outer_containers = driver.find_elements(By.CLASS_NAME, 'rt-connection-sameday')

        for outer in outer_containers:
            departure_datetime = self._get_result_departure_date(outer)
            inner_containers = outer.find_elements(By.CLASS_NAME, 'rt-connection-container')

            for inner in inner_containers:
                yield self._process_result_inner_container(inner, departure_datetime)

    def _process_result_inner_container(self, inner, departure_datetime):
        time_table_selector = inner.find_element(By.CLASS_NAME, 'rt-connection-timetable')

        departure_time = self._get_route_time(time_table_selector, 'selectorDeparture')
        departure_datetime = datetime.combine(departure_datetime, convert_str_to_time(departure_time))
        arrival_time = self._get_route_time(time_table_selector, 'selectorArrival')
        arrival_datetime = combine_date_with_time(departure_datetime, arrival_time)
        price = self._get_route_price(inner)

        spider_item = SpiderItem(
            self._request.departure_place,
            self._request.arrival_place,
            departure_datetime,
            arrival_datetime,
            price,
            self.TRAVEL_AGENCY
        )
        print(spider_item)
        return spider_item

    @staticmethod
    def _get_route_time(time_table_selector, class_name):
        time_labels_departure = time_table_selector.find_elements(By.CLASS_NAME, class_name)
        return time_labels_departure[0].text.split("\n")[1]

    @staticmethod
    def _get_result_departure_date(outer_container):
        date = outer_container.find_element(By.CSS_SELECTOR, '.container > .rt-connection-date').text
        return datetime.strptime(date, "%A %d %b %Y")

    @staticmethod
    def _get_route_price(inner_container):
        price = inner_container.find_element(By.CSS_SELECTOR,
                                             'span[data-bind="text:secondClassButton.priceLabel"]').text
        price = price.split(" ")[0]
        return Money(amount=float(price), currency=DsbEuropeSpider.DEFAULT_CURRENCY)

    def _print_route(self, departure_datetime, arrival_datetime, price):
        print(
            f"Departure: {self._request.departure_place}, "
            f"Departure datetime: {convert_datetime_to_str(departure_datetime)}, "
            f"Arrival: {self._request.arrival_place}, "
            f"Arrival datetime: {convert_datetime_to_str(arrival_datetime)}, "
            f"Price: {price}"
        )

    @staticmethod
    def _click_button(driver, by, value):
        button = driver.find_element(by, value)
        button.click()
        sleep(.2)
