from pydantic import BaseModel


class EventIn(BaseModel):
    event: dict
