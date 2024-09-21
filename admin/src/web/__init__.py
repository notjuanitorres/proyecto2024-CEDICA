from flask import Flask
from flask_session import Session
from web.helpers.auth import is_authenticated
from src.core.config import config
from src.core import database
from src.core.bcrypt import bcrypt
from src.core.wiring import init_wiring
from src.web.handlers import error
from src.web.routes import register_blueprints
from src.core.commands import register_commands

session = Session()


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])

    database.init_app(app)
    session.init_app(app)
    bcrypt.init_app(app)

    register_blueprints(app)
    register_commands(app)
    init_wiring()

    error_codes = [400, 401, 403, 404, 405, 500]
    for code in error_codes:
        app.register_error_handler(code, error.handle_error)

    app.jinja_env.globals.update(is_authenticated=is_authenticated)

    return app
