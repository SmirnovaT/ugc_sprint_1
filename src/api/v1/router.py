from flask import Blueprint

from api.v1.events import router as events_router

v1_router = Blueprint("v1", __name__, url_prefix="/v1")

v1_router.register_blueprint(events_router)
