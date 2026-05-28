from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "PokeStats"
    SERVICE_PORT: int = 8001
    DATABASE_PATH: str = "data/poke_stats.db"
    LOG_FILE: str = "logs/poke-stats-service.log"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()