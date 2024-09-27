from flask import Blueprint, render_template, request, redirect, url_for, session
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from dependency_injector.wiring import inject, Provide


equestrian_bp = Blueprint(
    "equestrian_bp", __name__, template_folder="../templates/equestrian", url_prefix="/ecuestre"
)


@equestrian_bp.route("/")
@check_user_permissions(permissions_required=["ecuestre_index"])
def get_page():
    return render_template("horses.html")


@equestrian_bp.route("/<int:horse_id>")
def show_horse():
    pass


@equestrian_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_new"])
def create_horse():
    # create_form = EquestrianCreateForm()
    # if not check_user_permissions(permissions_required=["ecuestre_new"]):
    #     return redirect(url_for("index_bp.home"))

    if request.method == "POST":
        return add_horse()

    return render_template("create_horse.html")


def add_horse():
    # if not create_form.validate_on_submit():
    #     return render_template("create_horse.html", form=create_form)

    # equestrian_services.create_horse(
    #     {
    #         "name": create_form.name.data,
    #     }
    # )

    return redirect(url_for("equestrian_bp.get_page"))