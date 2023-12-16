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
from datetime import date, datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from backend.config import get_basic_crawler_process_settings
from backend.spiders.db_sipder import DBSpider
from backend.spiders.spider_base import SpiderRequest


if __name__ == "__main__":
    process = CrawlerProcess(get_basic_crawler_process_settings())
    process.crawl(DBSpider, request=SpiderRequest("Berlin Hb", "Hamburg Hb", datetime(2023, 12, 31)))
    process.start()

    # print(flixbus_scrape("Berlin", 'Copenhagen', '01.12.2023'))

