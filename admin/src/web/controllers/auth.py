from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.core.container import Container
from src.core.module.accounts import AbstractAccountsServices as AAS
from src.core.module.accounts import UserLoginForm, UserRegisterForm
from src.web.helpers.auth import is_authenticated


auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="../templates/accounts", url_prefix="/auth"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return authenticate()

    if is_authenticated(session):
        return redirect(url_for("index_bp.home"))

    login_form = UserLoginForm()
    return render_template("login.html", form=login_form)


@inject
def authenticate(accounts_services: AAS = Provide[Container.accounts_services]):
    login_form = UserLoginForm()

    if not login_form.validate_on_submit():
        return render_template("login.html", form=login_form)

    user = accounts_services.authenticate(
        login_form.email.data, login_form.password.data
    )

    if not user:
        flash("Email o contraseña inválida", "danger")
        return redirect(url_for("auth_bp.login"))

    session["user"] = user["id"]
    session["user_name"] = user["alias"]
    session["is_authenticated"] = True

    flash("Sesion iniciada correctamente, bienvenido/a.", "success")

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
    if request.method == "POST":
        return register_user()

    registration_form = UserRegisterForm()

    return render_template("register.html", form=registration_form)


@inject
def register_user(accounts_services: AAS = Provide[Container.accounts_services]):
    registration_form = UserRegisterForm()

    if not registration_form.validate_on_submit():
        return render_template("register.html", form=registration_form)

    accounts_services.create_user(
        {
            "email": registration_form.email.data,
            "alias": registration_form.alias.data,
            "password": registration_form.password.data,
        }
    )
    flash("Registro exitoso.", "success")
    flash("Tienes que esperar a que el administrador del sistema te habilite el acceso para ingresar", "warning")
    return redirect(url_for("index_bp.home"))
