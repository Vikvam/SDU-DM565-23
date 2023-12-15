from datetime import datetime

from scrapy.crawler import CrawlerProcess

from backend.config import get_basic_crawler_process_settings
from backend.spiders.flixbus_spider import FlixbusSpider
from backend.spiders.spider_base import SpiderRequest

if __name__ == "__main__":
    process = CrawlerProcess(
        get_basic_crawler_process_settings()
    )
    # process.crawl(FlixbusSpider, request=FlixbusRequest("Berlin", "Copenhagen", date(2023, 12, 31)))
    # print("---------------------")
    process.crawl(FlixbusSpider, request=SpiderRequest("Praha", "Mnichov", datetime(year=2024, month=1, day=31)))
    process.start()

    # print(flixbus_scrape("Berlin", 'Copenhagen', '01.12.2023'))
