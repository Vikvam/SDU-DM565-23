from importlib import import_module

import scrapy
from scrapy import signals, Request
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


# Partially adapted from by: https://github.com/clemfromspace/scrapy-selenium/


class SeleniumRequest(Request):
    def __init__(self, wait_timeout=5, do_before=None, wait_until=None, screenshot=False, script=None, *args, **kwargs):
        """Initialize a new selenium request
        Parameters
        ----------
        wait_timeout: int
            The number of seconds to wait.
        wait_until: method
            One of the "selenium.webdriver.support.expected_conditions".
            The response will be returned until the given condition is fulfilled.
        screenshot: bool
            If True, a screenshot of the page will be taken and the data of the screenshot
            will be returned in the response "meta" attribute.
        script: str
            JavaScript code to execute.
        """
        self.wait_timeout = wait_timeout
        self.do_before = do_before
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script = script
        super().__init__(*args, **kwargs)


class SeleniumMiddleware:
    def __init__(self, driver_name, driver_executable_path, driver_arguments):
        driver_service_module = import_module(f"selenium.webdriver.{driver_name}.service")
        driver_service_class = getattr(driver_service_module, "Service")
        driver_options_class = getattr(webdriver, f"{driver_name.capitalize()}Options")
        driver_class = getattr(webdriver, driver_name.capitalize())
        service = driver_service_class(executable_path=driver_executable_path)
        options = driver_options_class()
        for argument in driver_arguments:
            options.add_argument(argument)
        self.driver = driver_class(options, service)

    @classmethod
    def from_crawler(cls, crawler):
        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')
        if driver_name is None:
            raise NotConfigured('SELENIUM_DRIVER_NAME must be set')
        if driver_executable_path is None:
            raise NotConfigured('Either SELENIUM_DRIVER_EXECUTABLE_PATH must be set')
        middleware = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments
        )
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request: Request, spider: scrapy.Spider) -> HtmlResponse:
        """Process a request using the selenium driver if applicable"""
        if not isinstance(request, SeleniumRequest): return None
        self.driver.get(request.url)
        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie({"name": cookie_name, "value": cookie_value})
        if request.do_before:
            request.do_before(self.driver)
        if request.wait_until:
            WebDriverWait(self.driver, request.wait_timeout).until(request.wait_until)
        if request.screenshot:
            request.meta["screenshot"] = self.driver.get_screenshot_as_png()
        if request.script:
            self.driver.execute_script(request.script)
        body = str.encode(self.driver.page_source)
        request.meta.update({'driver': self.driver})
        return HtmlResponse(self.driver.current_url, body=body, request=request)

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""
        self.driver.quit()
