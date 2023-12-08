from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base_scraper import BaseScraper
import constants as const


@dataclass
class DsbRoute:
    line_name: str
    time: str
    cost: str


class DsbScraper(BaseScraper):
    def __init__(self, driver_path):
        super().__init__(driver_path, const.DSB_BASE_URL)

    def find_routes(self, departure, arrival):
        self._get_landing_page()
        self._accept_cookies()
        self._fill_search_input_fields(departure, arrival)
        self._wait_for_search_results()
        return self._retrieve_route_details()

    def _accept_cookies(self):
        accept_btn = self.find_element(
            By.CSS_SELECTOR, 'button[onclick="CookieInformation.submitAllCategories();"]')
        accept_btn.click()

    def _fill_search_input_fields(self, departure, arrival):
        departure_input = self.find_element(By.NAME, 'criteria[0].DepartLocation.Name')
        arrival_input = self.find_element(By.NAME, 'criteria[0].ArriveLocation.Name')
        search_button = self.find_element(By.ID, 'formSubmitBtn')

        self._fill_single_search_input(departure_input, departure)
        self._fill_single_search_input(arrival_input, arrival)
        search_button.click()

    def _fill_single_search_input(self, form_input, value):
        form_input.send_keys(value)

        wait = WebDriverWait(self, 2)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'autocomplete__link')
        ))
        autocomplete_link = self.find_element(By.CLASS_NAME, 'autocomplete__link')
        autocomplete_link.click()

    def _wait_for_search_results(self):
        wait = WebDriverWait(self, 10)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'journey')
        ))

    def _retrieve_route_details(self):
        possible_options = self.find_elements(By.CLASS_NAME, 'journey')
        routes = []

        for option in possible_options:
            route = DsbRoute(
                self._get_value_from_element(option, By.CLASS_NAME, 'journey-shift__text'),
                self._get_value_from_element(option, By.CLASS_NAME, 'journey-times__time'),
                self._get_value_from_element(option, By.CLASS_NAME, 'journey-lowestprice__headline')
            )
            routes.append(route)

        return routes
