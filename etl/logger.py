import logging
import sys

from config import settings


def setup_logger():
    """Настройка логгирования для приложения и backoff"""
    logger = logging.getLogger("etl")
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(level=settings.log_level.upper())

    logging.getLogger("backoff").addHandler(logging.StreamHandler())
