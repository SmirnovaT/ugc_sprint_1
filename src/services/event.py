from pydantic import ValidationError

from models.event import EVENT_REGISTRY, BaseEvent, EventEnvelope
from repositories.event import BaseEventRepo, get_rabbit_event_repo
from schemas.events import EventIn


class EventBaseError(Exception):
    """Базовая ошибка сервиса аналитических событий"""

    def __init__(self, detail=None) -> None:
        self.detail = detail


class EventValidationError(EventBaseError):
    """Ошибка валидации"""


class EventTypeError(EventBaseError):
    """Незарегистрированный тип события"""

    def __init__(self) -> None:
        self.detail = "данный тип события не зарегистрирован"


class EventService:
    def __init__(self, event_repo: BaseEventRepo) -> None:
        self.event_repo = event_repo

    async def process_event(self, raw_event: dict) -> None:
        # TODO: валидацию схемы запроса вынести в слой view/использовать библиотеку?
        try:
            event_envelope = EventEnvelope.model_validate(raw_event)
        except ValidationError as e:
            raise EventValidationError(detail=e.errors()) from e

        base_event = event_envelope.event
        EventModel = EVENT_REGISTRY.get(base_event.type)
        if not EventModel:
            raise EventTypeError

        try:
            EventModel.model_validate(base_event.data)
        except ValidationError as e:
            raise EventValidationError(detail=e.errors()) from e
        await self.event_repo.send_event(event_envelope)


def get_event_service():
    rabbit_event_repo = get_rabbit_event_repo()
    return EventService(event_repo=rabbit_event_repo)
