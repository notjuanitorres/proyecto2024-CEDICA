from flask import Blueprint, render_template, request, redirect, url_for, flash
from dependency_injector.wiring import inject, Provide
from src.core.module.accounts import UserCreateForm, UserEditForm
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
def create_user():
    if request.method == "POST":
        return add_user()

    create_form = UserCreateForm()
    return render_template("create_user.html", form=create_form)


@users_bp.route("/crear", methods=["POST"])
@inject
def add_user(accounts_services: AAS = Provide[Container.accounts_services]):
    create_form = UserCreateForm()

    if not create_form.validate_on_submit():
        return render_template("create_user.html", form=create_form)

    accounts_services.create_user(
        {
            "email": create_form.email.data,
            "alias": create_form.alias.data,
            "password": create_form.password.data,
            "enabled": create_form.enabled.data,
            "system_admin": create_form.system_admin.data,
            # 'role_id':create_form.role_id.data,
        }
    )

    # TODO: change redirect to user page when exists
    return redirect(url_for("users_bp.get_page"))


@users_bp.route("/editar/<int:user_id>")
@inject
def edit_user(user_id: int, accounts_services: AAS = Provide[Container.accounts_services]):
    if request.method in ["POST", "PUT"]:
        return update_user(user_id)

    user = accounts_services.get_user(user_id)
    
    if not user:
        redirect(url_for("users_bp.get_page"))
        
    edit_form = UserEditForm(data=user)

    return render_template("edit_user.html", form=edit_form)


@users_bp.route("/editar/<int:user_id>", methods=["POST", "PUT"])
@inject
def update_user(user_id: int, accounts_services: AAS = Provide[Container.accounts_services]):
    user = accounts_services.get_user(user_id=user_id)
    edit_form = UserEditForm(current_email=user['email'])
    if not edit_form.validate_on_submit():
        return render_template("edit_user.html", form=edit_form)

    accounts_services.update_user(
        user_id=user_id,
        data={
            "email": edit_form.email.data,
            "alias": edit_form.alias.data,
            "enabled": edit_form.enabled.data,
            "system_admin": edit_form.system_admin.data,
            # 'role_id':create_form.role_id.data,
        },
    )

    # TODO: change redirect to user page when exists
    return redirect(url_for("users_bp.get_page"))


@users_bp.route("/delete/", methods=["POST"])
@inject
def delete_user(accounts_services: AAS = Provide[Container.accounts_services]):
    user_id = request.form["item_id"]
    deleted = accounts_services.delete_user(user_id)
    if not deleted:
        flash("El usuario no ha podido ser eliminado, intentelo nuevamente", "danger")

    flash("El usuario ha sido eliminado correctamente", "success")
    return redirect(url_for("users_bp.get_page"))