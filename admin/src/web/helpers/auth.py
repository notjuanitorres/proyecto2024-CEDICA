from functools import wraps
from flask import session, redirect, url_for
from src.core.container import Container
from dependency_injector.wiring import inject, Provide
from typing import List


def is_authenticated(user_session):
    return user_session.get("user") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)

    return decorated_function


# @inject
# def check_user_permissions_decorator(permissions_required: List[str], accounts_services=Provide[Container.accounts_services]):
#     def decorator(f):  # need extra decorator because im passing an argument
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not is_authenticated(session):
#                 return redirect(url_for("auth_bp.login"))
#             user_permissions = accounts_services.get_permissions_of(session.get("user"))
#             for permission in permissions_required:
#                 if permission not in user_permissions:
#                     return redirect(url_for("auth_bp.login"))
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

def check_user_permissions(permissions_required, accounts_services=Provide[Container.accounts_services]):
    if not is_authenticated(session):
        return False

    if accounts_services.is_sys_admin(session.get("user")):
        return True

    user_permissions = accounts_services.get_permissions_of(session.get("user"))
    for permission in permissions_required:
        if permission not in user_permissions:
            return False
    
    return True


def inject_session_data():
    return dict(
        user_id=session.get("user"),
        user_name=session.get("user_name"),
        is_authenticated=is_authenticated(session),
        is_admin=session.get("is_admin"),
        permissions=session.get("permissions")
    )
