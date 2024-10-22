from functools import wraps
from flask import flash, redirect, url_for, session


def check_creation_in_process(session_name: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get(f"{session_name}"):
                flash("Oops. Solo se puede acceder creando una entidad")
                return redirect(url_for("index_bp.home"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator

