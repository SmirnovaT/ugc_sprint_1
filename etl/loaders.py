import logging

import backoff
import clickhouse_connect
from clickhouse_connect.driver.exceptions import Error, OperationalError
from config import ClickhouseSettings

from models import Event

logger = logging.getLogger("etl")


class ClickhouseLoader:
    def __init__(self, settings: ClickhouseSettings) -> None:
        self.settings = settings
        self.connect()

    @backoff.on_exception(
        backoff.expo,
        OperationalError,
        max_tries=10,
        max_time=10,
    )
    def connect(self):
        self.client = clickhouse_connect.get_client(
            host=self.settings.host,
            database=self.settings.database,
            username=self.settings.user,
            password=self.settings.password,
        )

    @backoff.on_exception(
        backoff.expo,
        OperationalError,
        max_tries=10,
        max_time=10,
    )
    def load_batch(self, event_batch: list[Event]):
        if not event_batch:
            return
        column_names = list(Event.model_fields.keys())
        data = tuple(tuple(event.model_dump().values()) for event in event_batch)
        try:
            result = self.client.insert(
                table=self.settings.table, data=data, column_names=column_names
            )
        except Error:
            logger.exception(f"error while loading batch into clickhouse {data}")
        else:
            logger.info(f"loaded batch {event_batch} with result {result.summary}")
