from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.core.container import Container
from src.core.module.user.mappers import UserMapper
from src.core.module.auth import AbstractAuthServices as AAS, UserLoginForm, UserRegisterForm
from src.web.helpers.auth import is_authenticated


auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="../templates/accounts", url_prefix="/auth"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if is_authenticated(session):
        return redirect(url_for("index_bp.home"))

    login_form = UserLoginForm()

    if request.method == "POST":
        return authenticate(login_form=login_form)

    return render_template("login.html", form=login_form)


@inject
def authenticate(login_form: UserLoginForm, auth_services: AAS = Provide[Container.auth_services]):
    if not login_form.validate_on_submit():
        return render_template("login.html", form=login_form)

    user = auth_services.authenticate(
        login_form.email.data, login_form.password.data
    )

    if not user:
        flash("Email o contraseña inválida", "danger")
        return render_template("login.html", form=login_form)

    session["user"] = user["id"]
    session["user_name"] = user["alias"]
    session["is_authenticated"] = True
    session["is_admin"] = user["system_admin"]
    permissions = auth_services.get_permissions_of(user["id"])
    session["permissions"] = permissions

    flash("Sesión iniciada correctamente, bienvenido/a.", "success")

    return redirect(url_for("index_bp.home"))


@auth_bp.post("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("Sesión cerrada", "success")

    return redirect(url_for("index_bp.home"))


@auth_bp.route("/registrarse", methods=["GET", "POST"])
def register():
    if is_authenticated(session):
        flash("Ya estás autenticado", "info")
        return redirect(url_for("index_bp.home"))

    registration_form = UserRegisterForm()

    if request.method == "POST":
        return register_user(registration_form=registration_form)

    return render_template("register.html", form=registration_form)


@inject
def register_user(registration_form: UserRegisterForm, user_repository: AAS = Provide[Container.user_repository]):
    if not registration_form.validate_on_submit():
        return render_template("register.html", form=registration_form)

    user_repository.add(UserMapper.to_entity(registration_form.data))
    flash("Registro exitoso.", "success")
    flash("Tienes que esperar a que el administrador del sistema te habilite el acceso para ingresar", "warning")
    return redirect(url_for("index_bp.home"))
