from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class KafkaSettings(BaseModel):
    host: str
    port: int
    topic: str


class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    project_name: str = "ugc_service"
    app_port: int = 8000
    kafka: KafkaSettings
    api_url: str

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
    private_key: str = "secret"
    public_key: str = "secret"


settings = Settings()
