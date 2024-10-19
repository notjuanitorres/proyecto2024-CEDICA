from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dependency_injector.wiring import inject, Provide
from src.core.module.user import (
    UserCreateForm,
    UserEditForm,
    AbstractUserRepository,
    UserSearchForm,
    UserMapper,
)
from src.core.module.employee import AbstractEmployeeRepository
from src.core.container import Container


users_bp = Blueprint(
    "users_bp", __name__, template_folder="./accounts/user", url_prefix="/usuarios"
)


@users_bp.before_request
@inject
def require_login_and_sys_admin(user_repository=Provide[Container.user_repository]):
    if not user_repository.is_sys_admin(session.get("user")):
        return redirect(url_for("auth_bp.login"))


@users_bp.route("/")
@inject
def get_users(
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    page = request.args.get("page", type=int)
    need_archive = bool(request.args.get("archive", default=False))
    search = UserSearchForm(request.args)
    search_query = {}
    order_by = []
    search_query["filters"] = {"is_deleted": need_archive}
    if search.submit_search.data and search.validate():
        order_by = [(search.order_by.data, search.order.data)]
        search_query = {
            "text": search.search_text.data,
            "field": search.search_by.data,
        }
        if search.filter_enabled.data:
            search_query["filters"] = {"enabled": search.filter_enabled.data}
        if search.filter_role_id.data:
            search_query["filters"]["role_id"] = int(search.filter_role_id.data)

    paginated_users = user_repository.get_page(
        page=page, order_by=order_by, search_query=search_query
    )

    return render_template(
        "users.html" if not need_archive else "users_archived.html",
        users=paginated_users,
        search_form=search,
    )


@users_bp.route("/<int:user_id>")
@inject
def show_user(
    user_id: int,
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    user = user_repository.get_user(user_id)
    assigned_to = user.get("assigned_to")
    if not user:
        flash(f"El usuario con ID = {user_id} no existe", "danger")
        return redirect(url_for("user_bp.get_users"))
    employee: dict | None = None
    if assigned_to:
        employee = employees.get_employee(assigned_to)
    return render_template("user.html", user=user, employee=employee)


@users_bp.route("/crear", methods=["GET", "POST"])
def create_user():
    create_form = UserCreateForm()

    if request.method == "POST":
        return add_user(create_form=create_form)

    return render_template("create_user.html", form=create_form)


@inject
def add_user(
    create_form: UserCreateForm,
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    if not create_form.validate_on_submit():
        return render_template("create_user.html", form=create_form)

    user = user_repository.add(UserMapper.to_entity(create_form.data, is_creation=True))

    flash("Usuario creado correctamente", "success")
    if create_form.submit_another.data:
        return redirect(url_for("users_bp.create_user"))

    return redirect(url_for("users_bp.show_user", user_id=user["id"]))


@users_bp.route("/editar/<int:user_id>", methods=["GET", "POST", "PUT"])
@inject
def edit_user(
    user_id: int,
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    user = user_repository.get_user(user_id)

    if user.get("system_admin"):
        flash("No se puede editar a un administrador del sistema")
        return redirect(url_for("users_bp.get_users"))

    if not user or user.get("is_deleted"):
        flash("El usuario no existe")
        return redirect(url_for("users_bp.get_users"))

    edit_form = UserEditForm(data=user, current_email=user["email"])

    if request.method in ["POST", "PUT"]:
        return update_user(user_id=user_id, edit_form=edit_form)

    return render_template("edit_user.html", form=edit_form)


@inject
def update_user(
    user_id: int,
    edit_form: UserEditForm,
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    if not edit_form.validate_on_submit():
        return render_template("edit_user.html", form=edit_form)

    user_repository.update(
        user_id=user_id,
        data={
            "email": edit_form.email.data,
            "alias": edit_form.alias.data,
            "system_admin": edit_form.system_admin.data,
            "role_id": edit_form.role_id.data,
        },
    )

    return redirect(url_for("users_bp.show_user", user_id=user_id))


@users_bp.route("/archivar/", methods=["POST"])
@inject
def archive_user(
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    user_id = request.form["item_id"]
    archived = user_repository.archive(user_id)

    if not archived:
        flash("El usuario no existe o no puede ser archivado", "warning")

    flash("El usuario ha sido archivado correctamente", "success")
    return redirect(url_for("users_bp.show_user", user_id=user_id))

@users_bp.route("/recuperar/", methods=["POST"])
@inject
def recover_user(
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    user_id = request.form.get("user_id")
    recovered = user_repository.recover(user_id)

    if not recovered:
        flash("El usuario no existe o no puede ser recuperado", "warning")

    flash("El usuario ha sido recuperado correctamente", "success")
    return redirect(url_for("users_bp.show_user", user_id=user_id))


@users_bp.route("/eliminar/", methods=["POST"])
@inject
def delete_user(
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    user_id = request.form["item_id"]
    deleted = user_repository.delete(user_id)

    if not deleted:
        flash("El usuario no ha podido ser eliminado, intentelo nuevamente", "danger")

    flash("El usuario ha sido eliminado correctamente", "success")
    return redirect(url_for("users_bp.get_users", archive=True))


@users_bp.route("/toggle-activacion/<int:user_id>")
@inject
def toggle_activation(
    user_id: int,
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    toggled = user_repository.toggle_activation(user_id)

    if not toggled:
        flash("No se puede desactivar a un administrador del sistema", "danger")
    else:
        flash("La operacion fue un exito", "success")

    return redirect(request.referrer or url_for("index_bp.home"))
