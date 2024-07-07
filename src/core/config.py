from logging import config as logging_config
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


BASE_DIR = Path(__file__).resolve().parent.parent.parent



class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    project_name: str = "ugc_service"
    app_port: int = 8000

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
