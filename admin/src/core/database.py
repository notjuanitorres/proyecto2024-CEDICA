from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """
    Initializes the database with the Flask application.

    This function sets up the SQLAlchemy extension with the provided Flask app
    and configures the necessary hooks for database session management.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        Flask: The Flask application instance with the database initialized.
    """
    db.init_app(app)
    configure_hooks(app)
    return app


def configure_hooks(app):
    """
    Configures hooks for the database.

    This function sets up a teardown hook to close the database session
    at the end of each request.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        Flask: The Flask application instance with hooks configured.
    """

    @app.teardown_appcontext
    def close_session(exception=None):
        """
        Closes the database session.

        This function is called automatically at the end of each request
        to close the database session.

        Args:
            exception (Exception, optional): An optional exception that occurred during the request.
        """
        db.session.close()

    return app


def reset(app):
    """
        Resets the database by dropping and recreating all tables.

        This function drops all existing tables in the database and recreates them.
        It should be called within the app context to ensure proper table creation.
        Models that want to be included in the schema should be imported here

        Args:
            app (Flask): The Flask application instance.
        """
    # Necessary to create the tables with create_all
    # It should have the app context
    # pylint: disable=C0415,W0611
    from .module.equestrian.models import Horse
    from .module.user.models import User
    from .module.auth.models import Role, Permission, RolePermission
    from .module.employee.models import Employee
    from .module.payment.models import Payment

    with app.app_context():
        print("Dropping the database... ")
        db.drop_all()
        print("Recreating the database... ")
        db.create_all()
        print("Done!")
