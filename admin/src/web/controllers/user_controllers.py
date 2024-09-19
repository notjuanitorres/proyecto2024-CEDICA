from flask import Blueprint, render_template
from dependency_injector.wiring import inject, Provide
from src.core.container import Container

users_bp = Blueprint(
    "users_bp", __name__, template_folder="../templates/user", url_prefix="/usuarios"
)


@users_bp.route("/")
@inject
def get_users(user_service=Provide[Container.user_services]):
    return render_template('users.html')


@users_bp.route("/<int:user_id>")
@inject
def get_user(user_service=Provide[Container.user_services]):
    pass


@users_bp.route("/create", methods=["POST"])
@inject
def create_user(user_service=Provide[Container.user_services]):
    pass


@users_bp.route("/update/<int:user_id>")
@inject
def update_user(user_service=Provide[Container.user_services]):
    pass


@users_bp.route("/delete/<int:user_id>")
@inject
def delete_user(user_service=Provide[Container.user_services]):
    pass
