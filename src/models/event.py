from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class EventsEnum(StrEnum):
    CLICK = "click"
    PAGE_VIEW_TIME = "page_view_time"
    FILM_QUALITY = "film_quality"
    FILM_WATCHED = "film_watched"
    SEARCH_FILTER = "search_filter"


class BaseEvent(BaseModel):
    type: EventsEnum
    timestamp: datetime
    user_id: UUID | None = None
    fingerprint: str
    data: dict


class EventEnvelope(BaseModel):
    event: BaseEvent


EVENT_REGISTRY: dict[EventsEnum, type[BaseModel]] = {}


def register_event(event_type: EventsEnum):
    def decorator(event_class):
        EVENT_REGISTRY[event_type] = event_class
        return event_class

    return decorator


@register_event(EventsEnum.CLICK)
class ClickEvent(BaseModel):
    element: str


@register_event(EventsEnum.PAGE_VIEW_TIME)
class PageViewTimeEvent(BaseModel):
    url: str
    time: int


@register_event(EventsEnum.FILM_QUALITY)
class FilmQualityEvent(BaseModel):
    film: str
    id_film: UUID
    original_quality: int
    updated_quality: int


@register_event(EventsEnum.FILM_WATCHED)
class FilmWatchedEvent(BaseModel):
    id_film: UUID
    film: str


@register_event(EventsEnum.SEARCH_FILTER)
class SearchFilterEvent(BaseModel):
    filter: str
