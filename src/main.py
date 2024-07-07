from flask import Flask

from api.router import api_router


def create_app(test_config=None) -> Flask:
    # create and configure the app
    app = Flask(__name__)

    app.register_blueprint(api_router)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
