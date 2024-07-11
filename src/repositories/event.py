import logging
from abc import ABC, abstractmethod

from aiokafka import AIOKafkaProducer

from core.config import settings
from models.event import EventEnvelope

logger = logging.getLogger(__name__)


class BaseEventRepo(ABC):
    """Абстрактный базовый класс для репозитория аналитических событий"""

    @abstractmethod
    async def send_event(self, event: EventEnvelope) -> None:
        """Метод для отправки события в брокер/хранилище"""


class KafkaEventRepo(BaseEventRepo):
    """Репозиторий аналитических событий использующий Kafka в качестве брокера"""

    def __init__(self) -> None:
        # кажется not thread safe, потому создаем каждый раз
        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=f"{settings.kafka.host}:{settings.kafka.port}"
        )
        self.topic = settings.kafka.topic

    async def send_event(self, event: EventEnvelope) -> None:
        """Метод для отправки события в брокер/хранилище"""
        await self.kafka_producer.start()
        message = event.model_dump_json()
        try:
            await self.kafka_producer.send_and_wait(
                topic=self.topic, value=message.encode()
            )
        except Exception:
            logger.exception(f"error while sending message to kafka {message=}")
        finally:
            await self.kafka_producer.stop()


def get_kafka_event_repo() -> KafkaEventRepo:
    return KafkaEventRepo()
