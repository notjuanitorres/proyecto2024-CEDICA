from flask import Blueprint, render_template, request, redirect, url_for, flash
from dependency_injector.wiring import inject, Provide
from src.core.module.employee import AbstractEmployeeRepository
from src.core.module.employee.forms import TrainerSearchForm, TrainerSelectForm, EmployeeSearchForm
from src.core.module.common import AbstractStorageServices, FileMapper
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.equestrian.forms import (
    HorseCreateForm,
    HorseEditForm, 
    HorseSearchForm,
    HorseAddDocumentsForm,
    HorseDocumentSearchForm
)
from src.core.module.equestrian import AbstractEquestrianRepository
from src.core.module.equestrian.mappers import HorseMapper

equestrian_bp = Blueprint(
    "equestrian_bp", __name__, template_folder="../templates/equestrian", url_prefix="/ecuestre"
)


@inject
def search_horses(search: HorseSearchForm,
                  need_archived: bool = False,
                  equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    """
    Helper function to search horses.

    Args:
        search (HorseSearchForm): The form for searching horses.
        need_archived (bool): Indicates if the search should include archived horses.
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Pagination: The paginated list of horses.
    """

    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    order_by = []
    search_query = {
        "filters": {
            "is_archived": need_archived
        }
    }

    if search.submit_search.data and search.validate():
        order_by = [(search.order_by.data, search.order.data)]
        search_query = {
            "text": search.search_text.data,
            "field": search.search_by.data,
        }
        if search.filter_ja_type.data:
            search_query["filters"] = {"ja_type": search.filter_ja_type.data}

    return equestrian_repository.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )


@equestrian_bp.route("/")
@check_user_permissions(permissions_required=["ecuestre_index"])
@inject
def get_horses():
    """
    Route to get a paginated list of horses.

    Returns:
        Response: The rendered template for the list of horses.
    """
    search = HorseSearchForm(request.args)

    paginated_horses = search_horses(search=search, need_archived=False)

    return render_template("./equestrian/horses.html", horses=paginated_horses, search_form=search)


@equestrian_bp.route("/archivados", methods=["GET"])
@check_user_permissions(permissions_required=["ecuestre_index"])
def get_archived_horses():
    """
    Route to get a paginated list of archived horses.

    Returns:
        Response: The rendered template for the list of archived horses.
    """
    search_form = HorseSearchForm(request.args)
    paginated_horses = search_horses(search=search_form, need_archived=True)
    return render_template(
        "./equestrian/horses_archived.html",
        horses=paginated_horses,
        search_form=search_form,
    )


@equestrian_bp.route("/archivar/", methods=["POST"])
@check_user_permissions(permissions_required=["ecuestre_destroy"])
@inject
def archive_horse(
        horses_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
):
    """
    Route to archive a horse.

    Args:
        horses_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: Redirect to the horse details.
    """
    horse_id = request.form["item_id"]
    archived = horses_repository.archive_horse(int(horse_id))
    if not archived:
        flash("El caballo no existe o ya ha sido archivado", "warning")
    else:
        flash("El caballo ha sido archivado correctamente", "success")
    return redirect(url_for("equestrian_bp.show_horse", horse_id=horse_id))


@equestrian_bp.route("/recuperar/", methods=["POST"])
@check_user_permissions(permissions_required=["ecuestre_destroy"])
@inject
def recover_horse(
        horses: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
):
    """
    Route to recover a horse.

    Args:
        horses (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: Redirect to the horse details.
    """
    horse_id = request.form["horse_id"]
    recovered = horses.recover_horse(int(horse_id))
    if not recovered:
        flash("El caballo no existe o no puede ser recuperado", "warning")
    else:
        flash("El caballo ha sido recuperado correctamente", "success")
    return redirect(url_for("equestrian_bp.show_horse", horse_id=horse_id))


@equestrian_bp.route("/<int:horse_id>")
@check_user_permissions(permissions_required=["ecuestre_show"])
@inject
def show_horse(horse_id: int,
               equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    """
    Route to show details of a specific horse.

    Args:
        horse_id (int): The ID of the horse.
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: The rendered template for the horse details if the horse exists,
         otherwise redirect to the list of horses.
    """
    horse = equestrian_repository.get_by_id(horse_id, documents=True)
    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return get_horses()

    trainers = equestrian_repository.get_trainers_of_horse(horse_id)
    return render_template('./equestrian/horse.html', horse=horse, horse_trainers=trainers)


@equestrian_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_new"])
def create_horse():
    """
    Route to create a new horse.

    Returns:
        Response: The rendered template for creating a horse.
    """
    create_form = HorseCreateForm()

    if request.method == "POST":
        return add_horse(create_form=create_form)

    return render_template("./equestrian/create_horse.html", form=create_form)


@inject
def add_horse(create_form: HorseCreateForm,
              equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    """
    Helper function to add a new horse.

    Args:
        create_form (HorseCreateForm): The form for creating a horse.
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: The rendered template for creating a horse if the form wasn't valid
         or redirect to document creation.
    """
    if not create_form.validate_on_submit():
        return render_template("./equestrian/create_horse.html", form=create_form)

    horse = equestrian_repository.add(HorseMapper.to_entity(create_form.data, []))

    flash("Caballo creado con exito!", "success")
    return redirect(url_for("equestrian_bp.create_document", horse_id=horse["id"]))


@equestrian_bp.route("/editar/<int:horse_id>/documentos/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def create_document(horse_id: int,
                    equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    """
    Route to create a new document for a horse.

    Args:
        horse_id (int): The ID of the horse.
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: The rendered template for creating a document if horse exists,
         otherwise redirect to the list of horses.
    """
    horse = equestrian_repository.get_by_id(horse_id)
    if not horse:
        flash(f"El caballo con ID = {horse_id} no existe", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    create_form = HorseAddDocumentsForm()
    if request.method == "POST":
        return add_document(horse=horse, create_form=create_form)

    return render_template("./equestrian/create_document.html", form=create_form, horse=horse)


@inject
def add_document(horse,
                 create_form: HorseAddDocumentsForm,
                 equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
                 storage: AbstractStorageServices = Provide[Container.storage_services]):
    """
    Helper function to add a new document to a horse.

    Args:
        horse (dict): The horse data.
        create_form (HorseAddDocumentsForm): The form for adding a document.
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.
        storage (AbstractStorageServices): The storage service.

    Returns:
        Response: The rendered template for creating a document if form wasn't valid or redirect to document creation.
    """
    if not create_form.validate_on_submit():
        return render_template("./equestrian/create_document.html", form=create_form, horse=horse)

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
    """
    Route to edit a horse's details.

    Args:
        horse_id (int): The ID of the horse.
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: The rendered template for editing a horse if the horse exists,
        otherwise redirect to the list of horses.
    """
    horse = equestrian_repository.get_by_id(horse_id)

    if not horse:
        flash(f"Su búsqueda no devolvió un caballo existente", "danger")
        return redirect(url_for("equestrian_bp.get_horses"))

    if horse.get("is_archived"):
        flash("No se puede editar un caballo archivado", "danger")
        return redirect(url_for("equestrian_bp.show_horse", horse_id=horse_id))

    edit_form = HorseEditForm(data=horse)

    if request.method in ["POST", "PUT"]:
        return update_horse(horse_id=horse_id, edit_form=edit_form)

    return render_template("./equestrian/edit_horse.html", form=edit_form, horse=horse)


@inject
def update_horse(horse_id: int, edit_form: HorseEditForm,
                 equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    """
    Helper function to update a horse's details.

    Args:
        horse_id (int): The ID of the horse.
        edit_form (HorseEditForm): The form for editing a horse.
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: The rendered template for editing a horse if the form wasn't valid or redirect to horse details.
    """
    if not edit_form.validate_on_submit():
        return render_template("./equestrian/edit_horse.html", form=edit_form)

    equestrian_repository.update(
        horse_id=horse_id,
        data=HorseMapper.from_simple_form(edit_form.data),
    )

    flash("Caballo actualizado con éxito", "success")
    return redirect(url_for("equestrian_bp.show_horse", horse_id=horse_id))


@equestrian_bp.route("/delete/", methods=["POST"])
@check_user_permissions(permissions_required=["ecuestre_destroy"])
@inject
def delete_horse(equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository]):
    """
    Route to delete a horse.

    Args:
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: Redirect to the list of horses.
    """
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
):
    """
        Route to edit documents of a horse.

        Args:
            horse_id (int): The ID of the horse.
            equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

        Returns:
            Response: The rendered template for editing documents.
        """
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

    return render_template(
        "./equestrian/update_documents.html",
        horse=horse,
        files=paginated_files,
        add_form=add_document_form,
        search_form=search_document_form,
        paginated_files=paginated_files,
    )


@equestrian_bp.route("/editar/<int:horse_id>/documentos/eliminar", methods=["POST"])
@check_user_permissions(permissions_required=["ecuestre_update"])
@inject
def delete_document(
        horse_id: int,
        equestrian_repository: AbstractEquestrianRepository = Provide[Container.equestrian_repository],
        storage: AbstractStorageServices = Provide[Container.storage_services],
):
    """
        Route to delete a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            equestrian_repository (AbstractEquestrianRepository): The equestrian repository.
            storage (AbstractStorageServices): The storage service.

        Returns:
            Response: Redirect to the document editing page
        """
    document_id = int(request.form["item_id"])
    document = equestrian_repository.get_document(horse_id, document_id)

    if not document:
        flash(f"El documento solicitado no existe", "danger")
        return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))

    if not document.get("is_link"):
        deleted_in_bucket = storage.delete_file(document.get("path"))
        if not deleted_in_bucket:
            flash("No se ha podido eliminar el documento, inténtelo nuevamente", "danger")
            return redirect(url_for("equestrian_bp.edit_documents", horse_id=horse_id))

    deleted = equestrian_repository.delete_document(horse_id, document_id)
    if not deleted:
        flash("El documento no ha podido ser eliminado, inténtelo nuevamente", "danger")
    else:
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
    """
        Route to edit a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            document_id (int): The ID of the document.
            equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

        Returns:
            Response: The rendered template for editing a document if horse exists and document exists,
                otherwise redirect to the list of horses or the list of documents.
        """
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
    """
        Helper function to update a document of a horse.

        Args:
            horse (dict): The horse data.
            document (dict): The document data.
            edit_form (HorseAddDocumentsForm): The form for editing a document.
            equestrian_repository (AbstractEquestrianRepository): The equestrian repository.
            storage (AbstractStorageServices): The storage service.

        Returns:
            Response: The rendered template for editing a document if the form wasn't valid
             or redirect to document editing

        """
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
    """
        Route to link a trainer to a horse.

        Args:
            horse_id (int): The ID of the horse.
            horses (AbstractEquestrianRepository): The equestrian repository.
            employees (AbstractEmployeeRepository): The employee repository.

        Returns:
            Response: The rendered template for linking a trainer if the horse exists,
            otherwise redirect to the list of horses.
        """
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
    """
        Helper function to add a trainer to a horse.

        Args:
            horse (dict): The horse data.
            search_form (TrainerSearchForm): The form for searching trainers.
            select_form (TrainerSelectForm): The form for selecting a trainer.
            paginated_trainers (Pagination): The paginated list of trainers.
            horses (AbstractEquestrianRepository): The equestrian repository.

        Returns:
            Response: The rendered template for linking a trainer if the select form wasn't valid
            or redirect to horse trainers.
        """
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
    """
        Route to get the trainers of a horse.

        Args:
            horse_id (int): The ID of the horse.
            horses (AbstractEquestrianRepository): The equestrian repository.
            employees (AbstractEmployeeRepository): The employee repository.

        Returns:
            Response: The rendered template for the list of trainers if the horse exists,
             otherwise redirect to the list of horses.
        """
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
                         equestrian_repository: AbstractEquestrianRepository = Provide[
                             Container.equestrian_repository]):
    """
    Route to unlink a trainer from a horse.

    Args:
        horse_id (int): The ID of the horse.
        equestrian_repository (AbstractEquestrianRepository): The equestrian repository.

    Returns:
        Response: Redirect to the list of horse trainers.
    """
    trainer_id = request.form["item_id"]
    deleted = equestrian_repository.remove_horse_trainer(int(horse_id), int(trainer_id))
    if not deleted:
        flash("El entrenador no ha podido ser desvinculado, inténtelo nuevamente", "danger")
    else:
        flash("El entrenador ha sido desvinculado correctamente", "success")

    return redirect(url_for("equestrian_bp.get_horse_trainers", horse_id=horse_id))
