from logging import config as logging_config

import orjson
from flask.json.provider import JSONProvider
from flask_openapi3 import OpenAPI

from api.error_handling import setup_error_handling
from api.router import api_router
from core.config import settings
from core.logger import LOGGING


class OrJSONProvider(JSONProvider):
    def dumps(self, obj, *, option=None, **kwargs):
        if option is None:
            option = orjson.OPT_APPEND_NEWLINE | orjson.OPT_NAIVE_UTC

        return orjson.dumps(obj, option=option).decode()

    def loads(self, s, **kwargs):
        return orjson.loads(s)


def create_app() -> OpenAPI:
    logging_config.dictConfig(LOGGING)

    app = OpenAPI(__name__)

    app.json = OrJSONProvider(app)
    app.register_api(api_router)
    setup_error_handling(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=settings.app_port)
