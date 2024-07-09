from abc import ABC, abstractmethod

from models.event import EventEnvelope


class BaseEventRepo(ABC):
    """Абстрактный базовый класс для репозитория аналитических событий"""

    @abstractmethod
    async def send_event(self, event: EventEnvelope) -> None:
        """Метод для отправки события в брокер/хранилище"""


class RabbitEventRepo(BaseEventRepo):
    """Репозиторий аналитических событий использующий RabbitMQ в качестве брокера"""

    def __init__(self) -> None:
        super().__init__()

    async def send_event(self, event: EventEnvelope) -> None:
        """Метод для отправки события в брокер/хранилище"""
        # заглушка
        print(event.model_dump)


def get_rabbit_event_repo() -> RabbitEventRepo:
    return RabbitEventRepo()
