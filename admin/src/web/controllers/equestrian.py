from typing import Dict

from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.core.module.employee import AbstractEmployeeRepository
from src.core.module.employee.forms import TrainerSearchForm, TrainerSelectForm, EmployeeSearchForm
from src.core.module.common import AbstractStorageServices, FileMapper
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from dependency_injector.wiring import inject, Provide
from src.core.module.equestrian.forms import (HorseCreateForm,
                                              HorseEditForm, HorseSearchForm,
                                              HorseAddDocumentsForm,
                                              HorseDocumentSearchForm)
from src.core.module.equestrian import AbstractEquestrianRepository
from src.core.module.equestrian.models import FileTagEnum
from src.core.module.equestrian.mappers import HorseMapper

equestrian_bp = Blueprint(
    "equestrian_bp", __name__, template_folder="../templates/equestrian", url_prefix="/ecuestre"
)


@equestrian_bp.route("/")
@check_user_permissions(permissions_required=["ecuestre_index"])
@inject
def get_horses(equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
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

    if search_query.get("filters"):
        search_query["filters"]["is_deleted"] = False
    else:
        search_query["filters"] = {"is_deleted": False}

    paginated_horses = equestrian_repository.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )

    return render_template("horses.html", horses=paginated_horses, search_form=search)


@equestrian_bp.route("/<int:horse_id>")
@check_user_permissions(permissions_required=["ecuestre_show"])
@inject
def show_horse(horse_id: int,
               equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    horse = equestrian_repository.get_by_id(horse_id, documents=False)

    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return get_horses()

    trainers = equestrian_repository.get_trainers_of_horse(horse_id)
    return render_template('horse.html', horse=horse, horse_trainers=trainers)


@equestrian_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_new"])
def create_horse():
    create_form = HorseCreateForm()

    if request.method == "POST":
        return add_horse(create_form=create_form)

    return render_template("create_horse.html", form=create_form)


@inject
def add_horse(create_form: HorseCreateForm,
              equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
              ):
    if not create_form.validate_on_submit():
        return render_template("create_horse.html", form=create_form)

    horse = equestrian_repository.add(HorseMapper.to_entity(create_form.data, []))

    flash("Caballo creado con exito!", "success")
    return redirect(url_for("equestrian_bp.create_document", horse_id=horse["id"]))


@equestrian_bp.route("/editar/<int:horse_id>/documentos/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def create_document(horse_id: int,
                    equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    horse = equestrian_repository.get_by_id(horse_id)
    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    create_form = HorseAddDocumentsForm()
    if request.method == "POST":
        return add_document(horse=horse, create_form=create_form)

    return render_template("create_document.html", form=create_form, horse=horse)


@inject
def add_document(horse,
                 create_form: HorseAddDocumentsForm,
                 equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
                 storage: AbstractStorageServices = Provide[Container.storage_services],
                 ):
    if not create_form.validate_on_submit():
        return render_template("create_document.html", form=create_form, horse=horse)

    if create_form.upload_type.data == "file":
        uploaded_document = storage.upload_file(
            file=create_form.file.data, path=equestrian_repository.storage_path, title=create_form.title.data)

        if not uploaded_document:
            flash(f"No se pudo subir el archivo, inténtelo nuevamente", "danger")
            return redirect(url_for("equestrian_bp.create_document", horse_id=horse["id"]))
    else:
        uploaded_document = FileMapper.file_from_form(create_form.data)

    equestrian_repository.add_document(
        horse_id=horse["id"],
        document=HorseMapper.create_file(
            document_type=create_form.tag.data, file_information=uploaded_document
        ))

    flash(f"El documento {uploaded_document.get('title')} se ha subido exitosamente", "success")
    return redirect(url_for("equestrian_bp.create_document", horse_id=horse["id"]))


@equestrian_bp.route("/editar/<int:horse_id>", methods=["GET", "POST", "PUT"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def edit_horse(horse_id: int,
               equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    horse = equestrian_repository.get_by_id(horse_id)

    if not horse:
        flash(f"Su búsqueda no devolvió un caballo existente", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    edit_form = HorseEditForm(data=horse)

    if request.method in ["POST", "PUT"]:
        return update_horse(horse_id=horse_id, edit_form=edit_form)

    return render_template("edit_horse.html", form=edit_form, horse=horse)


@inject
def update_horse(horse_id: int, edit_form: HorseEditForm,
                 equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    if not edit_form.validate_on_submit():
        return render_template("edit_horse.html", form=edit_form)

    equestrian_repository.update(
        horse_id=horse_id,
        data=HorseMapper.from_simple_form(edit_form.data),
    )
    equestrian_repository.set_horse_trainers(horse_id, edit_form.trainers.data)

    return redirect(url_for("equestrian_bp.show_horse", horse_id=horse_id))


@equestrian_bp.route("/delete/", methods=["POST"])
@check_user_permissions(permissions_required=["ecuestre_destroy"])
@inject
def delete_horse(equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    horse_id = request.form["item_id"]
    deleted = equestrian_repository.delete(int(horse_id))
    if not deleted:
        flash("El caballo no ha podido ser eliminado, inténtelo nuevamente", "danger")
    else:
        flash("El caballo ha sido eliminado correctamente", "success")

    return redirect(url_for("equestrian_bp.get_horses"))


@equestrian_bp.route("/editar/<int:horse_id>/documentos/", methods=["GET"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def edit_documents(
        horse_id: int,
        equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
        storage: AbstractStorageServices = Provide[Container.storage_services],
):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)

    horse = equestrian_repository.get_by_id(horse_id=horse_id, documents=False)
    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    add_document_form = HorseAddDocumentsForm()
    search_document_form = HorseDocumentSearchForm(request.args)

    search_query = {}
    order_by = []
    if search_document_form.submit_search.data and search_document_form.validate():
        order_by = [(search_document_form.order_by.data, search_document_form.order.data)]
        search_query = {
            "text": search_document_form.search_text.data,
            "field": search_document_form.search_by.data,
        }
        if search_document_form.filter_tag.data:
            search_query["filters"] = {"tag": search_document_form.filter_tag.data}

    paginated_files = equestrian_repository.get_file_page(
        horse_id=horse_id, page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )

    documents = []
    for file in paginated_files:
        file = file.to_dict()
        if not file.get("is_link"):
            documents.append({"file": file, "download_url": storage.presigned_download_url(file.get("path"))})
        else:
            documents.append({"file": file, "download_url": None})

        if not documents[-1].get("file").get("is_link") and not documents[-1].get("download_url"):
            flash(f"Algunos archivos no se pudieron obtener", "warning")
            break

    return render_template(
        "./equestrian/update_documents.html",
        horse=horse,
        documents=documents,
        add_form=add_document_form,
        search_form=search_document_form,
        paginated_files=paginated_files,
    )


@equestrian_bp.route("/editar/<int:horse_id>/documentos/eliminar", methods=["POST"])
@inject
def delete_document(
        horse_id: int,
        equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
        storage: AbstractStorageServices = Provide[Container.storage_services],
):
    document_id = int(request.form["item_id"])
    document = equestrian_repository.get_document(horse_id, document_id)

    if not document.get("is_link"):
        deleted_in_bucket = storage.delete_file(document.get("path"))
        if not deleted_in_bucket:
            flash("No se ha podido eliminar el documento, inténtelo nuevamente", "danger")
            return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))

    equestrian_repository.delete_document(horse_id, document_id)
    flash(f"El documento {document.get("title")} ha sido eliminado correctamente", "success")

    return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))


@equestrian_bp.route("/editar/<int:horse_id>/documentos/editar/<int:document_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def edit_document(
        horse_id: int,
        document_id: int,
        equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
):
    horse = equestrian_repository.get_by_id(horse_id=horse_id, documents=False)
    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    document = equestrian_repository.get_document(horse_id, document_id)
    if not document:
        flash(f"El documento con ID = {document_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))

    edit_form = HorseAddDocumentsForm(data=FileMapper.to_form(document))
    if request.method == "POST":
        return update_document(horse, document, edit_form)

    return render_template(
        "./equestrian/edit_document.html",
        horse=horse,
        document=document,
        form=edit_form,
    )


@inject
def update_document(horse: dict,
                    document: dict,
                    edit_form: HorseAddDocumentsForm,
                    equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
                    storage: AbstractStorageServices = Provide[Container.storage_services], ):
    if not (edit_form.is_submitted()
            and
            edit_form.validate(is_file_already_uploaded=not document.get("is_link"))):
        return render_template(
            "./equestrian/edit_document.html",
            horse=horse,
            document=document,
            form=edit_form,
        )

    uploaded_document = {}
    if edit_form.upload_type.data == 'url':
        uploaded_document = FileMapper.file_from_form(edit_form.data)

    if edit_form.upload_type.data == 'file':
        if edit_form.file.data:
            uploaded_document = storage.upload_file(
                edit_form.file.data,
                equestrian_repository.storage_path,
                title=edit_form.title.data
            )
        else:
            uploaded_document = FileMapper.file_from_form(edit_form.data)

        if not uploaded_document:
            flash("No se pudo modificar el archivo, inténtelo nuevamente", "danger")
            return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse["id"]))

    success = equestrian_repository.update_document(
        horse_id=horse["id"],
        document_id=document["id"],
        data=uploaded_document,
    )

    if success:
        flash(f"El documento {edit_form.title.data} ha sido modificado correctamente", "success")
    else:
        flash(f"El documento {edit_form.title.data} no ha podido ser modificado", "danger")

    return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse["id"]))


@equestrian_bp.route("/sincronizar-entrenador/<int:horse_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def link_trainer(
        horse_id: int,
        horses: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
        employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    page = request.args.get("page", type=int, default=1)

    search_trainer = TrainerSearchForm(request.args)
    select_trainer = TrainerSelectForm()
    horse = horses.get_by_id(horse_id, documents=False)

    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    search_query = {}

    if request.method == "GET" and search_trainer.validate():
        search_fields = ["name", "email"]
        search_query = {"text": search_trainer.search_text.data, "fields": search_fields}

    search_query["filters"] = {"not_horse_id": horse_id}

    trainers = employees.get_paginated_trainers(
        page=page, search_query=search_query
    )

    if request.method == "POST":
        return add_horse_trainer(horse, search_trainer, select_trainer, trainers)

    return render_template(
        "./equestrian/update_trainer.html",
        horse=horse,
        trainers=trainers,
        search_form=search_trainer,
        select_form=select_trainer,
    )


@inject
def add_horse_trainer(
        horse,
        search_form,
        select_form,
        paginated_trainers,
        horses: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
):
    if not (select_form.submit_trainer.data and select_form.validate()):
        return render_template(
            "./equestrian/update_trainer.html",
            horse=horse,
            trainers=paginated_trainers,
            search_form=search_form,
            select_form=select_form,
        )

    horse_id = horse.get("id")
    trainer_id = select_form.selected_trainer.data

    horses.add_horse_trainers(horse_id, [trainer_id])

    flash(
        f"Se ha asociado correctamente a {horse.get('name')} con su entrenador",
        "success",
    )
    return redirect(url_for("equestrian_bp.get_horse_trainers", horse_id=horse_id))


@equestrian_bp.route("/ver-entrenadores/<int:horse_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_index"])
@inject
def get_horse_trainers(
        horse_id: int,
        horses: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
        employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("per_page", type=int)

    horse = horses.get_by_id(horse_id, documents=False)

    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    search = EmployeeSearchForm(request.args)
    search_query = {}
    order_by = []
    search_query["filters"] = {"only_horse_id": horse_id}

    trainers = employees.get_paginated_trainers(
        page=page, per_page=per_page, search_query=search_query, order_by=order_by
    )

    return render_template(
        "./equestrian/horse_trainers.html",
        horse=horse,
        trainers=trainers,
        search_form=search
    )


@equestrian_bp.route("/desvincular-entrenador/<int:horse_id>/", methods=["POST"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def unlink_horse_trainer(horse_id: int,
                         equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):

    trainer_id = request.form["item_id"]
    deleted = equestrian_repository.remove_horse_trainer(int(horse_id), int(trainer_id))
    if not deleted:
        flash("El entrenador no ha podido ser desvinculado, inténtelo nuevamente", "danger")
    else:
        flash("El entrenador ha sido desvinculado correctamente", "success")

    return redirect(url_for("equestrian_bp.get_horse_trainers", horse_id=horse_id))
