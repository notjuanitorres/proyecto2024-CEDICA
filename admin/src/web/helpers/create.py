from functools import wraps
from flask import flash, redirect, url_for, session


def check_creation_in_process(session_name: str):
    """
    Decorator to check if a creation process is in progress.

    This decorator checks if a specific session variable is set, indicating that
    a creation process is in progress. If the session variable is not set, it flashes
    a message and redirects the user to the home page.

    Args:
        session_name (str): The name of the session variable to check.

    Returns:
        function: The decorated function if the session variable is set, otherwise a redirect to the home page.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get(f"{session_name}"):
                flash("Oops. Solo se puede acceder creando una entidad")
                return redirect(url_for("index_bp.home"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator