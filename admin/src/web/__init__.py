from flask import Flask
from src.web.config import config
from src.web.handlers import error
from src.web.controllers.index import index_bp
from src.web.controllers.user import users_bp
from src.web.controllers.auth import auth_bp
from src.core import database
from src.core.container import Container
from flask_session import Session
from src.core.bcrypt import bcrypt
from web.helpers.auth import is_authenticated

session = Session()


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])

    #extensions
    database.init_app(app)
    session.init_app(app)
    bcrypt.init_app(app)

    container = Container()
    container.wire(modules=[__name__])

    app.register_blueprint(index_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)

    error_codes = [400, 401, 403, 404, 405, 500]
    for code in error_codes:
        app.register_error_handler(code, error.handle_error)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    app.jinja_env.globals.update(is_authenticated=is_authenticated)

    return app
