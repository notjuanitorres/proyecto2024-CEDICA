from functools import wraps
from flask import session
from flask import abort


def is_authenticated(user_session):
    return user_session.get("user") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if is_authenticated(session):
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function
