from http import HTTPStatus

from flask import Response, request
from flask_openapi3 import APIBlueprint

from models.event import EventEnvelope
from services.event import EventService, get_event_service
from utils.auth import validate_token

router = APIBlueprint("events", __name__, url_prefix="/events")


@router.post("/")
async def post_click_event(body: EventEnvelope):
    """Обработка события аналитики"""

    user_id = None
    if access_token := request.cookies.get("access_token"):
        user_id = validate_token(access_token).user_id

    event_service: EventService = get_event_service()
    await event_service.process_event(body, user_id)
    return Response(status=HTTPStatus.NO_CONTENT)
