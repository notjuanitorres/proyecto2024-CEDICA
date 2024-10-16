from typing import List
from functools import wraps
from flask import session, redirect, url_for
from dependency_injector.wiring import inject, Provide
from src.core.container import Container


def is_authenticated(user_session):
    return user_session.get("user") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)

    return decorated_function


def check_user_permissions(permissions_required: List[str]):
    def decorator(f):  # need extra decorator because im passing an argument
        @wraps(f)
        @inject
        def decorated_function(*args,
                               accounts_services=Provide[Container.accounts_services],
                               **kwargs):

            if (not is_authenticated(session) or
                    not accounts_services.is_user_enabled(session.get("user"))):
                return redirect(url_for("auth_bp.login"))

            if accounts_services.is_sys_admin(session.get("user")):
                return f(*args, **kwargs)

            user_permissions = accounts_services.get_permissions_of(session.get("user"))
            for permission in permissions_required:
                if permission not in user_permissions:
                    return redirect(url_for("auth_bp.login"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def inject_session_data():
    return dict(
        user_id=session.get("user"),
        user_name=session.get("user_name"),
        is_authenticated=is_authenticated(session),
        is_admin=session.get("is_admin", False),
        permissions=session.get("permissions", [])
    )
