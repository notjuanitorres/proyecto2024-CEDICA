from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

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
    Models that want to be included in the schema should be imported here
    """
    # Necessary to create the tables with create_all
    # It should have the app context
    # pylint: disable=C0415,W0611
    from .module.equestrian.models import Horse
    from .module.accounts.models import User
    from .module.employee.models import Employee
    from .module.jockey_amazon.models import JockeyAmazon

    with app.app_context():
        connection = db.engine.connect()
        print("Dropping the database... ")
        connection.execute(text("DROP TABLE IF EXISTS work_assignments CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS jockeys_amazons CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS horses CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        db.drop_all()
        print("Recreating the database... ")
        db.create_all()
        print("Done!")
