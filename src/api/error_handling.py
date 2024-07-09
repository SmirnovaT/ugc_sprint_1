from http import HTTPStatus

from flask import Flask, json
from werkzeug.exceptions import HTTPException

from services.event import EventBaseError


def handle_exceptions(e):
    """Обработка ошибок для Flask"""

    match e:
        case EventBaseError():
            return {"detail": e.detail}, HTTPStatus.BAD_REQUEST

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
            return {"detail": "internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR


def setup_error_handling(app: Flask):
    app.register_error_handler(Exception, handle_exceptions)
