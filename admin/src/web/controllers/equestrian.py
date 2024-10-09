from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from dependency_injector.wiring import inject, Provide
from src.core.module.equestrian.forms import HorseCreateForm, HorseEditForm, HorseSearchForm
from src.core.module.equestrian import AbstractEquestrianServices as AES

equestrian_bp = Blueprint(
    "equestrian_bp", __name__, template_folder="../templates/equestrian", url_prefix="/ecuestre"
)


@equestrian_bp.route("/")
@check_user_permissions(permissions_required=["ecuestre_index"])
@inject
def get_horses(equestrian_services: AES = Provide[Container.equestrian_services]):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    search = HorseSearchForm(request.args)
    search_query = {}
    order_by = []

    if search.submit_search.data and search.validate():
        order_by = [(search.order_by.data, search.order.data)]
        search_query = {
            "text": search.search_text.data,
            "field": search.search_by.data,
        }
        if search.filter_ja_type.data:
            search_query["filters"] = {"ja_type": search.filter_ja_type.data}

    paginated_horses = equestrian_services.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )

    return render_template("horses.html", horses=paginated_horses, search_form=search)


@equestrian_bp.route("/<int:horse_id>")
@check_user_permissions(permissions_required=["ecuestre_show"])
@inject
def show_horse(horse_id: int, equestrian_services: AES = Provide[Container.equestrian_services]):
    horse = equestrian_services.get_horse(horse_id)

    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return get_horses()

    trainers = equestrian_services.get_trainers_of_horse(horse_id)
    return render_template('horse.html', horse=horse, horse_trainers=trainers)


@equestrian_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_new"])
def create_horse():
    create_form = HorseCreateForm()

    if request.method == "POST":
        return add_horse(create_form=create_form)

    return render_template("create_horse.html", form=create_form)


@inject
def add_horse(create_form: HorseCreateForm, equestrian_services: AES = Provide[Container.equestrian_services]):
    if not create_form.validate_on_submit():
        return render_template("create_horse.html", form=create_form)

    horse = equestrian_services.create_horse(
        {
            "name": create_form.name.data,
            "breed": create_form.breed.data,
            "birth_date": create_form.birth_date.data,
            "coat": create_form.coat.data,
            "is_donation": create_form.is_donation.data,
            "admission_date": create_form.admission_date.data,
            "assigned_facility": create_form.assigned_facility.data,
            "ja_type": create_form.ja_type.data,
            "sex": create_form.sex.data,
        }
    )

    return redirect(url_for("equestrian_bp.show_horse", horse_id=horse["id"]))


@equestrian_bp.route("/editar/<int:horse_id>", methods=["GET", "POST", "PUT"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def edit_horse(horse_id: int, equestrian_services: AES = Provide[Container.equestrian_services]):
    horse = equestrian_services.get_horse(horse_id)

    if not horse:
        flash(f"Su búsqueda no devolvió un caballo existente", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    edit_form = HorseEditForm(data=horse)

    if request.method in ["POST", "PUT"]:
        return update_horse(horse_id=horse_id, edit_form=edit_form)

    return render_template("edit_horse.html", form=edit_form)


@inject
def update_horse(horse_id: int, edit_form: HorseEditForm,
                 equestrian_services: AES = Provide[Container.equestrian_services]):

    if not edit_form.validate_on_submit():
        return render_template("edit_horse.html", form=edit_form)

    equestrian_services.update_horse(
        horse_id=horse_id,
        data={
            "name": edit_form.name.data,
            "breed": edit_form.breed.data,
            "birth_date": edit_form.birth_date.data,
            "coat": edit_form.coat.data,
            "is_donation": edit_form.is_donation.data,
            "admission_date": edit_form.admission_date.data,
            "assigned_facility": edit_form.assigned_facility.data,
            "ja_type": edit_form.ja_type.data,
            "sex": edit_form.sex.data,
        },
    )
    equestrian_services.set_horse_trainers(horse_id, edit_form.trainers.data)

    return redirect(url_for("equestrian_bp.show_horse", horse_id=horse_id))


@equestrian_bp.route("/delete/", methods=["POST"])
@check_user_permissions(permissions_required=["ecuestre_destroy"])
@inject
def delete_horse(equestrian_services: AES = Provide[Container.equestrian_services]):
    horse_id = request.form["item_id"]
    deleted = equestrian_services.delete_horse(int(horse_id))
    if not deleted:
        flash("El caballo no ha podido ser eliminado, inténtelo nuevamente", "danger")

    flash("El caballo ha sido eliminado correctamente", "success")
    return redirect(url_for("equestrian_bp.get_horses"))
