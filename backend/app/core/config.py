from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with SQLite defaults for the MVP."""

    app_name: str = "Global Research Radar"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./global_research_radar.db"
    openalex_mailto: str | None = None
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    default_cluster_count: int = 6

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
