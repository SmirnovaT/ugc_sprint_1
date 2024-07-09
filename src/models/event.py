from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class EventsEnum(StrEnum):
    CLICK = "click"
    PAGE = "page"
    CHANGE_QUALITY = "change_quality"
    FILM_COMPLETED = "film_completed"
    SEARCH_FILTER = "search_filter"


class BaseEvent(BaseModel):
    type: EventsEnum
    timestamp: datetime
    user_id: UUID | None
    fingerprint: str


EVENT_REGISTRY: dict[EventsEnum, type[BaseEvent]] = {}


def register_event(event_type: EventsEnum):
    def decorator(event_class):
        EVENT_REGISTRY[event_type] = event_class
        return event_class

    return decorator


@register_event(EventsEnum.CLICK)
class ClickEvent(BaseEvent):
    element: str


@register_event(EventsEnum.PAGE)
class PageEvent(BaseEvent):
    url: str


@register_event(EventsEnum.CHANGE_QUALITY)
class ChangeQualityEvent(BaseEvent):
    original_quality: str
    updated_quality: str


@register_event(EventsEnum.FILM_COMPLETED)
class FilmCompletedEvent(BaseEvent):
    film_id: UUID
    film: str


@register_event(EventsEnum.SEARCH_FILTER)
class SearchFilterEvent(BaseEvent):
    filter: str
