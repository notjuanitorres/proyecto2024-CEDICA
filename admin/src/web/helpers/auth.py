from typing import List
from functools import wraps
from flask import session, redirect, url_for
from dependency_injector.wiring import inject, Provide
from src.core.container import Container
from src.core.module.auth import AbstractAuthServices


def is_authenticated(user_session):
    return user_session.get("user") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)

    return decorated_function


def check_user_permissions(permissions_required: List[str]):
    def decorator(f):  # need extra decorator because im passing an argument
        @wraps(f)
        @inject
        def decorated_function(
            *args,
            auth: AbstractAuthServices = Provide[Container.auth_services],
            **kwargs
        ):
            user_id = session.get("user")
            if not is_authenticated(session) or not auth.has_permissions(
                user_id, permissions_required
            ):
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
        permissions=session.get("permissions", []),
        profile_image_url=session.get("profile_image_url"),
    )
