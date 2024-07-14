import logging
from typing import Any

from pydantic import ValidationError

from models import Event

logger = logging.getLogger("etl")


def event_transformer(data: dict[str, Any]) -> Event:
    try:
        event = Event(**data["event"], **data["event"]["data"])
    except ValidationError:
        logger.exception(f"error while parsing event data {data}")
        raise
    else:
        return event
