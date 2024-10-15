from flask import Blueprint, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.jockey_amazon import (
    JockeyAmazonCreateForm,
    JockeyAmazonEditForm,
    JockeyAmazonSearchForm,
)
from src.core.module.jockey_amazon.models import jockey_amazon_enums as jockey_amazon_information
from src.core.module.jockey_amazon.models import EducationLevelEnum
from src.core.module.jockey_amazon.mappers import JockeyAmazonMapper as Mapper
from src.core.module.jockey_amazon.repositories import AbstractJockeyAmazonRepository

jockey_amazon_bp = Blueprint(
    "jockey_amazon_bp",
    __name__,
    template_folder="./templates/jockey_amazon/",
    url_prefix="/jockey_amazon/",
)

@jockey_amazon_bp.route("/", methods=["GET"])
@check_user_permissions(permissions_required=["jockey_amazon_index"])
@inject
def get_jockeys(
    jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    search = JockeyAmazonSearchForm(request.args)
    search_query = {}
    order_by = []

    if search.submit_search.data and search.validate():
        order_by = [(search.order_by.data, search.order.data)]
        search_query = {
            "text": search.search_text.data,
            "field": search.search_by.data,
        }

    paginated_jockeys_and_amazons = jockeys.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )

    return render_template(
        "./jockey_amazon/jockeys_amazons.html",
        jockeys=paginated_jockeys_and_amazons,
        jockey_amazon_information=jockey_amazon_information,
        search_form=search,
    )

@jockey_amazon_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["jockey_amazon_new"])
def create_jockey():

    create_form = JockeyAmazonCreateForm()
    if request.method == "POST":
        print(create_form.data)
        return add_jockey(create_form=create_form)
    return render_template(
        "./jockey_amazon/create_jockey_amazon.html",
        form=create_form,
        EducationLevelEnum=EducationLevelEnum
    )

@inject
def add_jockey(
    create_form,
    jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    if not create_form.validate_on_submit():
        print("Formulario no valido")
        print(create_form.errors)
        return render_template(
            "./jockey_amazon/create_jockey_amazon.html",
            form=create_form,
            EducationLevelEnum=EducationLevelEnum
        )
    print("Formulario valido")
    created_jockey = jockeys.add(Mapper.to_entity(create_form.data))
    flash("Jockey/Amazon creado con éxito!", "success")
    
    return redirect(
        url_for("jockey_amazon_bp.show_jockey", jockey_id=created_jockey["id"])
    )

@jockey_amazon_bp.route("/<int:jockey_id>")
@check_user_permissions(permissions_required=["jockey_amazon_show"])
@inject
def show_jockey(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    jockey = jockeys.get_jockey(jockey_id=jockey_id)
    if not jockey:
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    return render_template("./jockey_amazon/jockey_amazon.html", jockey=jockey)

@jockey_amazon_bp.route("/editar/<int:jockey_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def edit_jockey(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    jockey = jockeys.get_jockey(jockey_id)
    if not jockey:
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    update_form = JockeyAmazonEditForm(
        data=jockey,
        id=jockey_id,
        current_email=jockey["email"],
        current_dni=jockey["dni"],
    )

    if request.method == "POST":
        return update_jockey(update_form=update_form, jockey_id=jockey_id)

    return render_template(
        "./jockey_amazon/update_jockey_amazon.html", form=update_form, jockey=jockey
    )

@inject
def update_jockey(
    jockey_id: int,
    update_form,
    jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    jockey = jockeys.get_jockey(jockey_id)
    if not update_form.validate_on_submit():
        return render_template(
            "./jockey_amazon/update_jockey_amazon.html", form=update_form, jockey=jockey
        )

    if not jockeys.update(jockey_id, Mapper.flat_form(update_form.data)):
        flash("No se ha podido actualizar al Jockey/Amazon", "warning")
        return render_template("./jockey_amazon/update_jockey_amazon.html")

    flash("El Jockey/Amazon ha sido actualizado exitosamente ")
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey_id))

@jockey_amazon_bp.route("/delete/", methods=["POST"])
@inject
def delete_jockey(jockey_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository]):
    jockey_id = request.form["item_id"]
    deleted = jockey_repository.delete_jockey(jockey_id)
    if not deleted:
        flash("El Jockey/Amazon no ha podido ser eliminado, intentelo nuevamente", "danger")
    else:
        flash("El Jockey/Amazon ha sido eliminado correctamente", "success")

    return redirect(url_for("jockey_amazon_bp.get_jockeys"))