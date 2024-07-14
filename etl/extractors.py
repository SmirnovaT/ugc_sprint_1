import json
import logging
from typing import Any, AsyncIterator, Self

import backoff
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError, KafkaError
from config import KafkaSettings

logger = logging.getLogger("etl")


class KafkaExtractor:
    def __init__(self, settings: KafkaSettings):
        self.consumer = AIOKafkaConsumer(
            settings.topic,
            bootstrap_servers=f"{settings.host}:{settings.port}",
            auto_offset_reset="earliest",
            group_id=settings.group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

    @backoff.on_exception(
        backoff.expo,
        KafkaConnectionError,
        max_tries=10,
        max_time=10,
    )
    async def start(self) -> None:
        await self.consumer.start()

    async def close(self) -> None:
        await self.consumer.stop()

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, *args):
        await self.close()

    @backoff.on_exception(
        backoff.expo,
        KafkaConnectionError,
        max_tries=10,
        max_time=10,
    )
    async def extract(self) -> AsyncIterator[dict[str, Any]]:
        try:
            data = await self.consumer.getmany(timeout_ms=1000)
        except KafkaError:
            logging.exception("error while consuming messages from kafka")
        if not data:
            logger.info("got no new messages from kafka")
        for tp, messages in data.items():
            logger.info(f"got {len(messages)} messages from kafka topic {tp.topic}")
            for message in messages:
                logger.info(message.value)
                yield message.value
