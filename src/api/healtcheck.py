from http import HTTPStatus

from flask import Response

from api.router import api_router


@api_router.route("/health", methods=["GET"])
async def post_click_event():
    """Healthcheck"""
    return Response(status=HTTPStatus.NO_CONTENT)