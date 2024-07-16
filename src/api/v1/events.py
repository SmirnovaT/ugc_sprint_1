from http import HTTPStatus

import jwt
from flask import Response, request
from flask_openapi3 import APIBlueprint

from models.event import EventEnvelope
from services.event import EventService, get_event_service
from core.config import settings

router = APIBlueprint("events", __name__, url_prefix="/events")


@router.post("/")
async def post_click_event(body: EventEnvelope):
    """Обработка события аналитики"""

    event_service: EventService = get_event_service()
    access_token = request.cookies.get("access_token")
    user_id = jwt.decode(access_token,
                         key=settings.public_key,
                         algorithms=["RS256"])
    await event_service.process_event(body, user_id)
    return Response(status=HTTPStatus.NO_CONTENT)
