from flask import Blueprint, render_template, request, redirect, url_for
from dependency_injector.wiring import inject, Provide
from src.core.module.accounts import UserCreateForm
from src.core.container import Container
from src.core.module.accounts import AbstractAccountsServices as AAS

users_bp = Blueprint(
    "users_bp", __name__, template_folder="./accounts/user", url_prefix="/usuarios"
)


@users_bp.route("/")
@inject
def get_page(accounts_services: AAS = Provide[Container.accounts_services]):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    paginated_users = accounts_services.get_page(page, per_page)
    return render_template("users.html", users=paginated_users)


@users_bp.route("/<int:user_id>")
@inject
def show_user(accounts_services: AAS = Provide[Container.accounts_services]):
    pass


@users_bp.route("/crear")
@inject
def create_user(accounts_services: AAS = Provide[Container.accounts_services]):
    if request.method == "POST":
        return add_user()
    
    create_form = UserCreateForm()
    return render_template("create_user.html", form=create_form)


@users_bp.route("/crear", methods=["POST"])
@inject
def add_user(accounts_services: AAS = Provide[Container.accounts_services]):
    form = UserCreateForm()
    if form.validate_on_submit():
        pass
    
    return redirect(url_for('users_bp.get_page'))


@users_bp.route("/update/<int:user_id>")
@inject
def update_user(accounts_services: AAS = Provide[Container.accounts_services]):
    pass


@users_bp.route("/delete/<int:user_id>")
@inject
def delete_user(accounts_services: AAS = Provide[Container.accounts_services]):
    pass
