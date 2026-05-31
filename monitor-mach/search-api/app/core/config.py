from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "SearchAPI"
    SERVICE_PORT: int = 8000

    POKE_API_BASE_URL: str = "https://pokeapi.co/api/v2"
    POKE_STATS_BASE_URL: str = "http://localhost:8001"
    POKE_IMAGES_BASE_URL: str = "http://localhost:8002"

    HTTP_TIMEOUT_SECONDS: int = 10

    LOG_FILE: str = "logs/search-api.log"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()