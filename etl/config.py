from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class KafkaSettings(BaseModel):
    host: str = "localhost"
    port: int = 9092
    topic: str
    group_id: str 

class ClickhouseSettings(BaseModel):
    host: str = "localhost"
    port: int = 8123
    database: str = "example"
    user: str = "default"
    password: str = ""
    table: str = "events"


class Settings(BaseSettings):
    """Главный класс настроек всего приложения"""

    batch_size: int
    run_interval_seconds: int = 5
    run_once: bool = False
    log_level: str = "info"
    kafka: KafkaSettings
    ch: ClickhouseSettings

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
