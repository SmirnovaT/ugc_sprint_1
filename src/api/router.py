from http import HTTPStatus

from flask import Response
from flask_openapi3 import APIBlueprint, Response

from api.v1.router import v1_router

api_router = APIBlueprint("api", __name__, url_prefix="/api", abp_tags=[])
api_router.register_api(v1_router)


@api_router.get("/health")
async def post_click_event():
    """Healthcheck"""
    return Response(status=HTTPStatus.NO_CONTENT)
