import random
import uuid

from datetime import timezone, timedelta

import faker

fake = faker.Faker()


def generate_event(event_type, data_dict) -> dict:
    """Базовая функция для генерации событий"""

    return {
        "event": {
            "type": event_type,
            "timestamp": fake.date_time_this_year(
                before_now=True, after_now=False, tzinfo=timezone(timedelta(hours=3))
            ).isoformat(),
            "user_id": str(uuid.uuid4()),
            "fingerprint": f"{fake.user_agent()} {fake.random_int(min=1000, max=9999)}x{fake.random_int(min=1000, max=9999)} UTC+3; {fake.locale()} Windows; {str(uuid.uuid4())}",
            "data": data_dict,
        }
    }


def generate_click() -> dict:
    """Генерация данных для события 'Клик'"""

    return generate_event(
        "page_view_time",
        {
            "url": f"http://online-cinema/{fake.uri_path()}",
            "time": fake.random_int(min=1000, max=99999),
        },
    )


def generate_film_quality() -> dict:
    """Генерация данных для события 'Смена качества видео'"""

    return generate_event(
        "film_quality",
        {
            "id_film": str(uuid.uuid4()),
            "film": fake.catch_phrase(),
            "original_quality": random.choice([480, 720, 1080]),
            "updated_quality": random.choice([480, 720, 1080, 4]),
        },
    )


def generate_film_watched() -> dict:
    """Генерация данных для события 'Просмотр видео до конца'"""

    return generate_event(
        "film_watched",
        {
            "id_film": str(uuid.uuid4()),
            "film": fake.catch_phrase(),
        },
    )


def generate_page_view_time() -> dict:
    """Генерация данных для события 'Время просмотра страницы'"""

    return generate_event(
        "page_view_time",
        {
            "url": f"http://online-cinema/{fake.uri_path()}",
            "time": fake.random_int(min=1, max=300000),
        },
    )


def generate_page_visits() -> dict:
    """Генерация данных для события 'Количество просмотров страницы за активную сессию'"""

    return generate_event(
        "page_visits",
        {
            "url": f"http://online-cinema/{fake.uri_path()}",
            "count": random.randint(1, 100),
        },
    )


def generate_search_filter() -> dict:
    """Генерация данных для события 'Фильтры поиска'"""

    return generate_event(
        "search_filter",
        {
            "filter": fake.word(
                ext_word_list=["genre", "rating", "year", "actor", "film"]
            )
        },
    )
