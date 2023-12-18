from datetime import datetime
from scrapy.crawler import CrawlerProcess

<<<<<<< HEAD
from backend.config import get_basic_crawler_process_settings, get_pipeline_crawler_process_settings
=======
from backend.config import get_basic_crawler_process_settings
>>>>>>> origin/main
from backend.spiders.implementations.dsb_europe_spider import DsbEuropeSpider
from backend.spiders.implementations.db_sipder import DBSpider
from backend.spiders.implementations.flixbus_spider import FlixbusSpider
from backend.spiders.spider_base import SpiderRequest

if __name__ == "__main__":
<<<<<<< HEAD
    request = SpiderRequest("Fredericia", "Flensburg", datetime(year=2023, month=12, day=19))
    #request = SpiderRequest("Odense", "Hamburg ZOB", datetime(year=2023, month=12, day=19))

    process = CrawlerProcess(get_pipeline_crawler_process_settings())
    #process.crawl(FlixbusSpider, request)
=======
    request = SpiderRequest("Odense St.", "Hamburg Hbf", datetime(year=2024, month=1, day=31))

    process = CrawlerProcess(get_basic_crawler_process_settings())
    # process.crawl(FlixbusSpider, request)
>>>>>>> origin/main
    process.crawl(DsbEuropeSpider, request=request)
    process.start()
