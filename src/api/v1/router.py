from flask_openapi3 import APIBlueprint

from api.v1.events import router as events_router

v1_router = APIBlueprint("v1", __name__, url_prefix="/v1")

v1_router.register_api(events_router)
