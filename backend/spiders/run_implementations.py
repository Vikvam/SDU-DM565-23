from datetime import datetime
from scrapy.crawler import CrawlerProcess

from backend.config import get_basic_crawler_process_settings
from backend.spiders.implementations.dsb_europe_spider import DsbEuropeSpider
from backend.spiders.implementations.db_sipder import DBSpider
from backend.spiders.implementations.flixbus_spider import FlixbusSpider
from backend.spiders.spider_base import SpiderRequest

if __name__ == "__main__":
    request = SpiderRequest("Odense St.", "Hamburg Hbf", datetime(year=2024, month=1, day=31))

    process = CrawlerProcess(get_basic_crawler_process_settings())
    # process.crawl(FlixbusSpider, request)
    process.crawl(DsbEuropeSpider, request=request)
    process.start()
