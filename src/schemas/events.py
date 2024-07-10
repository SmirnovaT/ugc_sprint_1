from pydantic import BaseModel

from models.event import BaseEvent


class EventIn(BaseModel):
    event: dict