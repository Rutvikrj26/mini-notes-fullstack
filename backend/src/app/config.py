"""Application settings via pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "Mini Notes API"
    cors_origins: list[str] = ["http://localhost:5173"]
    host: str = "0.0.0.0"  # noqa: S104
    port: int = 8000
    log_level: str = "INFO"

    model_config = {"env_prefix": "APP_"}
