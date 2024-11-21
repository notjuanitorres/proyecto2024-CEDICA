from src.web.handlers.error import errors_bp
from src.web.controllers import (
    index_bp, auth_bp, users_bp, employee_bp,
    equestrian_bp, payment_bp, charges_bp, jockey_amazon_bp,
    contact_bp
)


def register_blueprints(app):
    """
    Registers all the blueprints with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(equestrian_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(jockey_amazon_bp)
    app.register_blueprint(charges_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(contact_bp)
