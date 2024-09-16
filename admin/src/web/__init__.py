from flask import Flask
from src.web.config import config
from src.web.handlers import error
from src.web.controllers.index import index_bp


def create_app(env="development", static_folder="static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])

    app.register_blueprint(index_bp, url_prefix="/")

    error_codes = [400, 401, 403, 404, 405, 500]
    for code in error_codes:
        app.register_error_handler(code, error.handle_error)

    return app
