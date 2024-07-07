from http import HTTPStatus

from flask import Blueprint, Response

from api.v1.router import v1_router

api_router = Blueprint("api", __name__, url_prefix="/api")
api_router.register_blueprint(v1_router)


@api_router.route("/health", methods=["GET"])
async def post_click_event():
    """Healthcheck"""
    return Response(status=HTTPStatus.NO_CONTENT)
