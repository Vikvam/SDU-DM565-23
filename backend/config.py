from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_maps_api_key: str
    selenium_driver_name: str
    selenium_driver_executable_path: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_crawler_process_settings():
    return {
        "DOWNLOADER_MIDDLEWARES": {
            "backend.spiders.selenium_middleware.SeleniumMiddleware": 800,
        },
        "ITEM_PIPELINES": {
            "backend.spiders.pipelines.RoutePipeline": 800
        },
        "DOWNLOAD_DELAY": 2,
        "SELENIUM_DRIVER_NAME": get_settings().selenium_driver_name,
        "SELENIUM_DRIVER_EXECUTABLE_PATH": get_settings().selenium_driver_executable_path,
        "SELENIUM_DRIVER_ARGUMENTS": [],  # ["--headless"],
        "LOG_LEVEL": "WARNING",
    }
