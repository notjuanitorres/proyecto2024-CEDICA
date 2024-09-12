from flask import Flask
from flask import render_template
from src.web.config import config
from src.web.handlers import error


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])

    @app.route("/")
    def home():
        return render_template("home.html")
    
    error_codes = [400, 401, 403, 404, 405, 500]

    for code in error_codes: 
        app.register_error_handler(code, error.handle_error)

    return app
