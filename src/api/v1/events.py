from http import HTTPStatus

from flask import Blueprint, Response, request

from services.event import EventService, get_event_service

router = Blueprint("events", __name__, url_prefix="/events")


@router.post("/")
async def post_click_event():
    """Обработка события аналитики"""

    event_data = request.get_json()
    event_service: EventService = get_event_service()
    await event_service.process_event(event_data)
    return Response(status=HTTPStatus.NO_CONTENT)
