from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from src.core import database
from src.core.config import config
from src.core.commands import register_commands
from src.core.bcrypt import bcrypt
from src.core.wiring import init_wiring
from src.web.routes import register_blueprints
from src.web.handlers import error
from src.web.helpers.auth import is_authenticated, inject_session_data
from src.web.helpers.filters import register_filters

csrf = CSRFProtect()
session = Session()


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])

    database.init_app(app)
    session.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    register_blueprints(app)
    register_commands(app)
    register_filters(app)
    init_wiring()

    error_codes = [400, 401, 403, 404, 405, 500]
    for code in error_codes:
        app.register_error_handler(code, error.handle_error)
    
    app.context_processor(inject_session_data)

    if app.config["SEED_ON_STARTUP"]:
        from src.core.seeds import seed_all
        from src.core.database import reset
        reset(app)
        seed_all(app)

    return app
