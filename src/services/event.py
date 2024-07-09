from pydantic import ValidationError

from models.event import EVENT_REGISTRY, BaseEvent
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

    async def process_event(self, event: dict) -> None:
        # TODO: валидацию схемы запроса вынести в слой view/использовать библиотеку?
        try:
            EventIn.model_validate(event).event
        except ValidationError as e:
            raise EventValidationError(detail=e.errors()) from e

        try:
            base_event = BaseEvent.model_validate(event["event"])
        except ValidationError as e:
            raise EventValidationError(detail=e.errors()) from e

        EventModel = EVENT_REGISTRY.get(base_event.type)
        if not EventModel:
            raise EventTypeError

        try:
            specific_event = EventModel.model_validate(event["event"])
        except ValidationError as e:
            raise EventValidationError(detail=e.errors) from e
        await self.event_repo.send_event(specific_event)


def get_event_service():
    rabbit_event_repo = get_rabbit_event_repo()
    return EventService(event_repo=rabbit_event_repo)
