import vertica_python

from generator_events.generate_to_db import generate_events
from test_db.test_vertica.config import connection_info
from test_db.test_utils.utils import time_it

TOTAL = 1000
BATCH_SIZE = 1000


def create_table():
    """Создание таблицы в БД"""
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS event (
            id IDENTITY,
            type VARCHAR NOT NULL,
            timestamp TIMESTAMP,
            user_id VARCHAR NOT NULL,
            fingerprint VARCHAR(256) NOT NULL,
            element VARCHAR NOT NULL,
            url VARCHAR NOT NULL)"""
        )


def insert_events(values):
    """Функция вставки записей пачками"""

    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        sql = """
            INSERT INTO event (type, timestamp, user_id, fingerprint, element, url)
            VALUES (%s, %s, %s, %s, %s, %s)"""

        cursor.executemany(sql, values)
        connection.commit()


@time_it(TOTAL)
def transform_data(event_generator):
    """Преобразование данных и вставка в БД"""

    for batch in event_generator:

        values = [
            (
                event["type"],
                event["timestamp"],
                event["user_id"],
                event["fingerprint"],
                event["element"],
                event["url"],
            )
            for event in batch
        ]

        insert_events(values)


@time_it(TOTAL)
def get_events(limit):
    """Получение всех записей из таблицы"""

    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        cursor.execute(f"""SELECT * FROM event LIMIT {limit}""")

        for row in cursor.iterate():
            print(row)


@time_it(TOTAL)
def update_events(limit):
    """Обновление 100000 записей"""

    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        query = f"""UPDATE event SET element = 'pic' 
        WHERE id in (SELECT id FROM event ORDER BY id LIMIT {limit})"""

        cursor.execute(query)
        connection.commit()


def drop_events():
    """Удаление таблицы"""

    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS event"""

        cursor.execute(query)
        connection.commit()


if __name__ == "__main__":
    create_table()
    event_generator = generate_events(count=TOTAL, batch_size=BATCH_SIZE)
    transform_data(event_generator)
    get_events(limit=TOTAL)
    update_events(limit=TOTAL)
    drop_events()
