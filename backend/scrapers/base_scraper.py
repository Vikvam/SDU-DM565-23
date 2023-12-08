from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service


class BaseScraper(webdriver.Chrome):
    def __init__(self, drive_path, base_url):
        self._driver_path = drive_path
        self._base_url = base_url
        super().__init__(service=Service(self._driver_path))

    def _get_landing_page(self):
        self.get(self._base_url)

    def _get_value_from_element(self, dom_element, by, value):
        return_value = None

        try:
            return_value = dom_element.find_element(by, value).text
        except NoSuchElementException:
            pass

        return return_value
