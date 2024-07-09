from logging import config as logging_config

import orjson
from flask import Flask
from flask.json.provider import JSONProvider

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


def create_app() -> Flask:
    logging_config.dictConfig(LOGGING)

    app = Flask(__name__)

    app.json = OrJSONProvider(app)
    app.register_blueprint(api_router)
    setup_error_handling(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=settings.app_port)
