from typing import Dict

from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.core.module.equestrian.mappers import HorseMapper
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
from src.core.module.equestrian.mappers import HorseMapper as Mapper

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

    paginated_horses = equestrian_repository.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )

    return render_template("horses.html", horses=paginated_horses, search_form=search)


@equestrian_bp.route("/<int:horse_id>")
@check_user_permissions(permissions_required=["ecuestre_show"])
@inject
def show_horse(horse_id: int,
               equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    horse = equestrian_repository.get_by_id(horse_id)

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
              storage: AbstractStorageServices = Provide[Container.storage_services],
              ):

    if not create_form.validate_on_submit():
        return render_template("create_horse.html", form=create_form)

    documents = create_form.documents.data
    uploaded_documents = [
        (tag.name, storage.upload_batch(documents.get(tag.name.lower()), equestrian_repository.storage_path))
        for tag in FileTagEnum
    ]
    horse = equestrian_repository.add(Mapper.to_entity(create_form.data, uploaded_documents))

    for doc in uploaded_documents:
        for file in doc[1]:
            if not file:
                flash(f"No se pudo subir el archivo {doc[0]}", "danger")
                return redirect(
                    url_for("equestrian_bp.show_horse", horse_id=horse["id"])
                )

    flash("Caballo creado con exito!", "success")
    return redirect(url_for("equestrian_bp.show_horse", horse_id=horse["id"]))


@equestrian_bp.route("/editar/<int:horse_id>", methods=["GET", "POST", "PUT"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def edit_horse(horse_id: int,
               equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    horse = equestrian_repository.get_by_id(horse_id)

    if not horse:
        flash(f"Su búsqueda no devolvió un caballo existente", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    trainers = [str(trainer.id) for trainer in equestrian_repository.get_trainers_of_horse(horse_id)]
    edit_form = HorseEditForm(data=horse, trainers=trainers)

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


@equestrian_bp.route("/editar/<int:horse_id>/documentos/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def edit_documents(
    horse_id: int,
    equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)

    horse = equestrian_repository.get_only_horse_by_id(horse_id=horse_id)
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

    if request.method == "POST":
        return update_documents(add_document_form, search_document_form, horse, documents, paginated_files)

    return render_template(
        "./equestrian/update_documents.html",
        horse=horse,
        documents=documents,
        add_form=add_document_form,
        search_form=search_document_form,
        paginated_files=paginated_files,
    )


@inject
def update_documents(
    add_form: HorseAddDocumentsForm,
    search_form: HorseDocumentSearchForm,
    horse: dict,
    documents: list[dict],
    paginated_files,
    equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    if not add_form.validate_on_submit():
        return render_template(
            "./equestrian/update_documents.html",
            add_form=add_form,
            horse=horse,
            documents=documents,
            search_form=search_form,
            paginated_files=paginated_files,
        )

    horse_id = horse["id"]
    if add_form.upload_type.data == 'file':
        uploaded_document = storage.upload_file(
            file=add_form.file.data, path=equestrian_repository.storage_path, title=add_form.title.data
        )
    else:
        uploaded_document = {
                    "path": add_form.url.data,
                    "filetype": None,
                    "filesize": None,
                    "title": add_form.title.data,
                    "is_link": True,
                }

    if not uploaded_document:
        flash("No se pudo subir el archivo, inténtelo nuevamente", "danger")
        return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))

    equestrian_repository.add_document(
        horse_id=horse_id,
        document=Mapper.create_file(
            document_type=add_form.tag.data, file_information=uploaded_document
        ),
    )
    flash(f"El documento {uploaded_document.get("title")} se ha subido exitosamente", "success")
    return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))


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
    horse = equestrian_repository.get_only_horse_by_id(horse_id=horse_id)
    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    document = equestrian_repository.get_document(horse_id, document_id)
    if not document:
        flash(f"El documento con ID = {document_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))

    edit_form = HorseAddDocumentsForm(data=FileMapper.to_form(document))
    if request.method == "POST":
        return update_document(horse_id, document_id, edit_form, document)

    return render_template(
        "./equestrian/edit_document.html",
        horse=horse,
        document=document,
        edit_form=edit_form,
    )


@inject
def update_document(horse_id: int,
                    document_id: int,
                    edit_form: HorseAddDocumentsForm,
                    previous_doc: Dict,
                    equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
                    storage: AbstractStorageServices = Provide[Container.storage_services],):

    was_file = not previous_doc["is_link"]
    if not (edit_form.is_submitted()
            and
            edit_form.validate(is_file_already_uploaded=was_file)):

        return render_template(
            "./equestrian/edit_document.html",
            horse_id=horse_id,
            document_id=document_id,
            edit_form=edit_form,
        )

    if edit_form.file.data and edit_form.upload_type.data == 'file':
        uploaded_document = storage.modify_file(edit_form.file.data, full_path=previous_doc["path"])
        if not uploaded_document:
            flash("No se pudo subir el archivo, inténtelo nuevamente", "danger")
            return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))

    if was_file and edit_form.upload_type.data == 'url':
        deleted_in_bucket = storage.delete_file(previous_doc["path"])
        if not deleted_in_bucket:
            flash("No se ha podido modificar el documento, inténtelo nuevamente", "danger")
            return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))

    success = equestrian_repository.update_document(
        horse_id=horse_id,
        document_id=document_id,
        data=Mapper.file_from_edit_form(edit_form.data),
    )
    if success:
        flash(f"El documento {edit_form.title.data} ha sido editado correctamente", "success")
    else:
        flash(f"El documento {edit_form.title.data} no ha podido ser editado", "danger")

    return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))


