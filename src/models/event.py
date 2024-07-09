from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class RolesEnum(StrEnum):
    CLICK = "click"
    PAGE = "page"
    CHANGE_QUALITY = "change_quality"
    FILM_COMPLETED = "film_completed"
    SEARCH_FILTER = "search_filter"


class BaseEvent(BaseModel):
    type: RolesEnum
    timestamp: datetime
    user_id: UUID | None
    fingerprint: str


class ClickEvent(BaseEvent):
    element: str


class PageEvent(BaseEvent):
    url: str


class ChangeQualityEvent(BaseEvent):
    original_quality: str
    updated_quality: str


class FilmCompletedEvent(BaseEvent):
    film_id: UUID
    film: str


class SearchFilterEvent(BaseEvent):
    filter: str


EVENT_TYPE_CLASS_MAP: dict[RolesEnum, type[BaseEvent]] = {
    RolesEnum.CLICK: ClickEvent,
    RolesEnum.CHANGE_QUALITY: ChangeQualityEvent,
    RolesEnum.PAGE: PageEvent,
    RolesEnum.CHANGE_QUALITY: ChangeQualityEvent,
    RolesEnum.FILM_COMPLETED: FilmCompletedEvent,
    RolesEnum.SEARCH_FILTER: SearchFilterEvent,
}
