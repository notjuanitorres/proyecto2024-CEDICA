from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """
    Initializes the database with the Flask application
    :param app: Flask application instance
    :return: app
    """
    db.init_app(app)
    configure_hooks(app)
    return app


def configure_hooks(app):
    """
    Configures hooks for the database
    :param app: Flask application instance
    :return: app
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()

    return app


def reset(app):
    """
    Resets the database by dropping and recreating all tables
    """
    # Necessary to create the tables with create_all
    # It should have the app context
    # pylint: disable=C0415,W0611
    from .module.accounts.models import User
    from .module.employee.models import Employee

    with app.app_context():
        print("Dropping the database... ")
        db.drop_all()
        print("Recreating the database... ")
        db.create_all()
        print("Done!")
