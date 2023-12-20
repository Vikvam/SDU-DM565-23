import logging
from functools import lru_cache

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from scrapy.settings import Settings as ScrapySettings

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    google_maps_api_key: str
    skyscanner_api_key: str
    selenium_driver_name: str
    selenium_driver_executable_path: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_basic_crawler_process_settings():
    return ScrapySettings({
        "DOWNLOADER_MIDDLEWARES": {
            "backend.spiders.selenium_middleware.SeleniumMiddleware": 800,
        },
        "SELENIUM_DRIVER_NAME": get_settings().selenium_driver_name,
        "SELENIUM_DRIVER_EXECUTABLE_PATH": get_settings().selenium_driver_executable_path,
        "SELENIUM_DRIVER_ARGUMENTS": [],  # ["--headless"],
        "LOG_LEVEL": "WARNING"
    }, priority=0)


@lru_cache
def get_pipeline_crawler_process_settings():
    settings = get_basic_crawler_process_settings()
    settings.set("ITEM_PIPELINES", {
        "backend.spiders.pipelines.RoutePipeline": 800
    })
    return settings


@lru_cache
def get_logging_settings():
    return {
        "level": logging.WARNING,
        "format": "%(asctime)s [%(name)s %(levelname)s]: %(message)s",
        "datefmt": "%H:%M:%S"
    }
