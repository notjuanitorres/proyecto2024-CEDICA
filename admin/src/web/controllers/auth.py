from flask import Blueprint
from flask import render_template
from flask import request, url_for, session, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.core.container import Container


auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="../templates/accounts", url_prefix="/auth"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("autenticando")
        return authenticate()

    return render_template("login.html")


@inject
def authenticate(accounts_services=Provide[Container.accounts_services]):
    params = request.form

    user = accounts_services.authenticate(params.get("email"), params.get("password"))

    if not user:
        flash("Email o contraseña inválida", "error")
        return redirect(url_for("auth_bp.login"))

    session["user"] = user.email
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
