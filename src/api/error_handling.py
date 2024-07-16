import logging
from http import HTTPStatus

from flask import Flask, json
from werkzeug.exceptions import HTTPException

from services.event import EventValidationError
from utils.auth import AuthTokenError

logger = logging.getLogger(__name__)


def handle_exceptions(e):
    """Обработка ошибок для Flask"""

    match e:
        case AuthTokenError():
            return {
                "detail": "access token is invalid or expired"
            }, HTTPStatus.UNAUTHORIZED

        case EventValidationError():
            return {"detail": e.detail}, HTTPStatus.UNPROCESSABLE_ENTITY

        case HTTPException():
            response = e.get_response()
            response.data = json.dumps(
                {
                    "code": e.code,
                    "detail": e.description,
                }
            )
            response.content_type = "application/json"
            return response

        case _:
            logging.exception("unhandled exception")
            return {"detail": "internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR


def setup_error_handling(app: Flask):
    app.register_error_handler(Exception, handle_exceptions)
