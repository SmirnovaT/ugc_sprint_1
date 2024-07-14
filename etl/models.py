from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    # общие
    type: str
    timestamp: datetime
    user_id: UUID | None = None
    fingerprint: str
    # специфические
    element: str | None = None
    url: str | None = None
    time: int | None = None
    id_film: UUID | None = None
    film: str | None = None
    original_quality: int | None = None
    updated_quality: int | None = None
    filter: str | None = None
