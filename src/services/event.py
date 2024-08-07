from pydantic import ValidationError

from models.event import EVENT_REGISTRY, EventEnvelope
from repositories.event import BaseEventRepo, get_kafka_event_repo


class EventBaseError(Exception):
    """Базовая ошибка сервиса аналитических событий"""

    def __init__(self, detail=None) -> None:
        self.detail = detail


class EventValidationError(EventBaseError):
    """Ошибка валидации"""


class EventTypeError(EventValidationError):
    """Незарегистрированный тип события"""

    def __init__(self) -> None:
        self.detail = "данный тип события не зарегистрирован"


class EventService:
    def __init__(self, event_repo: BaseEventRepo) -> None:
        self.event_repo = event_repo

    async def process_event(self, event_envelope: EventEnvelope, user_id: str) -> None:
        base_event = event_envelope.event
        base_event.user_id = user_id
        EventModel = EVENT_REGISTRY.get(base_event.type)
        if not EventModel:
            raise EventTypeError

        try:
            EventModel.model_validate(base_event.data)
        except ValidationError as e:
            raise EventValidationError(detail=e.errors()) from e
        await self.event_repo.send_event(event_envelope)


def get_event_service() -> EventService:
    kafka_event_repo = get_kafka_event_repo()
    return EventService(event_repo=kafka_event_repo)
