from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def init_app(app):
    """Initializes the bcrypt extension."""
    bcrypt.init_app(app)
