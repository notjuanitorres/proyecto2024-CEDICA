from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.core.container import Container
from src.core.module.accounts import UserLoginForm

auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="../templates/accounts", url_prefix="/auth"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return authenticate()

    login_form = UserLoginForm()
    return render_template("login.html", form=login_form)


@inject
def authenticate(accounts_services=Provide[Container.accounts_services]):
    login_form = UserLoginForm()

    user = accounts_services.authenticate(
        login_form.email.data, login_form.password.data
    )

    if not user:
        flash("Email o contraseña inválida", "error")
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


def register():
    pass
