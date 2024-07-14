import logging

from clickhouse_driver import Client

from generator_events.generate_to_db import generate_events
from test_db.test_utils.utils import time_it

TOTAL = 10000000
BATCH_SIZE = 100000


@time_it(TOTAL=TOTAL)
def transform_data(event_generator, insert_events):
    """Преобразование данных и вставка в БД"""
    logging.warning("Transforming data")
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


def insert_events(values):
    client.execute(
        """INSERT INTO event (type, timestamp, user_id, fingerprint, element, url)
            VALUES """,
        values,
    )


@time_it(TOTAL=TOTAL)
def get_events(limit):
    client.execute(f"""SELECT * FROM event LIMIT {limit}""")


@time_it(TOTAL=TOTAL)
def update_events(limit):
    client.execute(
        f"""ALTER TABLE event UPDATE element = 'pic' 
                WHERE id in (SELECT id FROM event ORDER BY id LIMIT {limit})"""
    )


def drop_events():
    client.execute("""DROP TABLE IF EXISTS event""")


print("In module products __package__, __name__ ==", __package__, __name__)

if __name__ == "__main__":
    client = Client(host="localhost")
    logging.warning("Creating a database")
    client.execute("CREATE DATABASE IF NOT EXISTS example ON CLUSTER company_cluster")
    drop_events()
    logging.warning("Creating a table")
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS event (
            id UInt32,
            type VARCHAR NOT NULL,
            timestamp VARCHAR,
            user_id VARCHAR NOT NULL,
            fingerprint VARCHAR(256) NOT NULL,
            element VARCHAR NOT NULL,
            url VARCHAR NOT NULL)
            ENGINE = MergeTree
            PRIMARY KEY id;"""
    )
    logging.warning("generating events")
    event_generator = generate_events(count=TOTAL, batch_size=BATCH_SIZE)
    transform_data(event_generator, insert_events)
    get_events(limit=TOTAL)
    update_events(limit=TOTAL)
    drop_events()
