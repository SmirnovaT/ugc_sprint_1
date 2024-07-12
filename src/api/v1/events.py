from http import HTTPStatus

from flask import Response
from flask_openapi3 import APIBlueprint

from models.event import EventEnvelope
from services.event import EventService, get_event_service

router = APIBlueprint("events", __name__, url_prefix="/events")


@router.post("/")
async def post_click_event(body: EventEnvelope):
    """Обработка события аналитики"""

    event_service: EventService = get_event_service()
    await event_service.process_event(body)
    return Response(status=HTTPStatus.NO_CONTENT)
