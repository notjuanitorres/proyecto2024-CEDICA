from functools import wraps
from flask import session, redirect, url_for


def is_authenticated(user_session):
    return user_session.get("user") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)

    return decorated_function
