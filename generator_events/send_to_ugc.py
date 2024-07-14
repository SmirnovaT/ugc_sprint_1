import random
import time

import requests
from events import (
    generate_click,
    generate_film_quality,
    generate_film_watched,
    generate_page_view_time,
    generate_search_filter,
)

# from ..src.core.config import settings

event_functions = [
    generate_click,
    generate_film_quality,
    generate_film_watched,
    generate_page_view_time,
    generate_search_filter,
]


def send_event(event: dict) -> None:
    """Функция отправки сгенерированных событий в ручку '/analytics_event'"""

    response = requests.post("http://127.0.0.1:8000/api/v1/events/", json=event, timeout=15)
    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    for i in range(100):
        random_function = random.choice(event_functions)
        event = random_function()
        send_event(event)
        time.sleep(1)
