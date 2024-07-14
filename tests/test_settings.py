from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class TestSettings(BaseSettings):
    api_url: str = "http://127.0.0.1:8000"


test_settings = TestSettings()
