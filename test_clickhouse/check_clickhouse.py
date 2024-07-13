from clickhouse_driver import Client

from generator_events.generate_to_db import generate_events
from test_utils.utils import time_it, transform_data

TOTAL = 10
BATCH_SIZE = 10

@time_it
def insert_events(values):
    client.execute(f"""
                INSERT INTO event (type, timestamp, user_id, fingerprint, element, url)
                VALUES ({values[0]}, {values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]})""")

@time_it
def get_events(limit):
    client.execute(f"""SELECT * FROM event LIMIT {limit}""")

@time_it
def update_events(limit):
    client.execute(f"""UPDATE event SET element = 'pic' 
                WHERE id in (SELECT id FROM event ORDER BY id LIMIT {limit})""")

def drop_events():
    client.execute("""DROP TABLE IF EXISTS event""")


print("In module products __package__, __name__ ==", __package__, __name__)

if __name__ == "__main__":
    client = Client(host='localhost')
    client.execute('CREATE DATABASE IF NOT EXISTS example ON CLUSTER company_cluster')
    client.execute("""
        CREATE TABLE IF NOT EXISTS event (
            id UInt32,
            type VARCHAR NOT NULL,
            timestamp TIMESTAMP,
            user_id VARCHAR NOT NULL,
            fingerprint VARCHAR(256) NOT NULL,
            element VARCHAR NOT NULL,
            url VARCHAR NOT NULL)
            ENGINE = MergeTree
            PRIMARY KEY id;""")

    event_generator = generate_events(count=TOTAL, batch_size=BATCH_SIZE)
    transform_data(event_generator, insert_events)
    get_events(limit=TOTAL)
    update_events(limit=TOTAL)
    drop_events()

