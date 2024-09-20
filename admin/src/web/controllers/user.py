from flask import Blueprint, render_template, request
from dependency_injector.wiring import inject, Provide
from src.core.container import Container

users_bp = Blueprint(
    "users_bp", __name__, template_folder="./templates/accounts/users", url_prefix="/usuarios"
)


@users_bp.route("/")
@inject
def get_page(accounts_services=Provide[Container.accounts_services]):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10)
    paginated_users = accounts_services.get_page(page, per_page)
    return render_template('users.html', users=paginated_users)


@users_bp.route("/<int:user_id>")
@inject
def show_user(accounts_services=Provide[Container.accounts_services]):
    pass


@users_bp.route("/create", methods=["POST"])
@inject
def create_user(accounts_services=Provide[Container.accounts_services]):
    pass


@users_bp.route("/update/<int:user_id>")
@inject
def update_user(accounts_services=Provide[Container.accounts_services]):
    pass


@users_bp.route("/delete/<int:user_id>")
@inject
def delete_user(accounts_services=Provide[Container.accounts_services]):
    pass
