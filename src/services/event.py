from logging import getLogger
from uuid import UUID, uuid4

from pydantic import ValidationError

from models.event import EVENT_TYPE_CLASS_MAP, BaseEvent

logger = getLogger()


class EventBaseError(Exception): ...


class EventBaseValidationError(EventBaseError): ...


class EventService:
    async def process_event(self, event: dict) -> None:
        try:
            base_event = BaseEvent.model_validate(event)
        except ValidationError as e:
            # TODO: обработать во вьюхе фласка
            raise EventBaseValidationError from e

        if EventModel := EVENT_TYPE_CLASS_MAP.get(base_event.type):
            try:
                specific_event = EventModel.model_validate(event)
            except ValidationError as e:
                raise EventBaseValidationError from e

            # TODO: подключить репозиторий очереди, отправить туда сообщение


def get_event_service():
    return EventService()
