from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_maps_api_key: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()