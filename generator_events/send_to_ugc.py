import time
import random
import requests

from core.config import settings
from generator_events.events import (
    generate_click,
    generate_film_quality,
    generate_film_watched,
    generate_page_view_time,
    generate_search_filter,
)

event_functions = [
    generate_click,
    generate_film_quality,
    generate_film_watched,
    generate_page_view_time,
    generate_search_filter,
]


def send_event(event: dict) -> None:
    """Функция отправки сгенерированных событий в ручку '/analytics_event'"""

    requests.post(settings.api_url, json=event, timeout=15)


if __name__ == "__main__":
    for i in range(100):
        random_function = random.choice(event_functions)
        event = random_function()
        send_event(event)
        time.sleep(1)
