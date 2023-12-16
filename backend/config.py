from functools import lru_cache

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    google_maps_api_key: str
    selenium_driver_name: str
    selenium_driver_executable_path: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_basic_crawler_process_settings():
    return {
        "DOWNLOADER_MIDDLEWARES": {
            "backend.spiders.selenium_middleware.SeleniumMiddleware": 800,
        },
        "SELENIUM_DRIVER_NAME": get_settings().selenium_driver_name,
        "SELENIUM_DRIVER_EXECUTABLE_PATH": get_settings().selenium_driver_executable_path,
        "SELENIUM_DRIVER_ARGUMENTS": ["--headless"],
        "LOG_LEVEL": "WARNING",
    }


@lru_cache
def get_pipeline_crawler_process_settings():
    settings = get_basic_crawler_process_settings()
    settings["ITEM_PIPELINES"] = {
        "backend.spiders.pipelines.RoutePipeline": 800
    }

    return settings
