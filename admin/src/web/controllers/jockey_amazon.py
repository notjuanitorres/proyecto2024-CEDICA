from flask import Blueprint, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide 
from src.core.module.common import AbstractStorageServices, FileMapper
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.jockey_amazon import (
    JockeyAmazonAddDocumentsForm,
    JockeyAmazonDocumentSearchForm,
    JockeyAmazonEditForm,
    JockeyAmazonSearchForm,
    jockey_amazon_enums as jockey_amazon_information,
    JockeyAmazonMapper as Mapper,
    AbstractJockeyAmazonRepository,
)
from .jockey_and_amazon import create_jockey_amazon_bp, update_jockey_amazon_bp


jockey_amazon_bp = Blueprint(
    "jockey_amazon_bp",
    __name__,
    template_folder="../templates/jockey_amazon/",
    url_prefix="/jockey_amazon",
)

jockey_amazon_bp.register_blueprint(create_jockey_amazon_bp)
jockey_amazon_bp.register_blueprint(update_jockey_amazon_bp)

@inject
def search_jockeys(
    search: JockeyAmazonSearchForm,
    need_archive: bool,
    jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("per_page", type=int, default=10)
    order_by = []
    search_query = {
        "filters": {
            "is_deleted": need_archive
        }
    }
    if search.submit_search.data and search.validate():
        order_by = [(search.order_by.data, search.order.data)]
        search_query["text"] = search.search_text.data
        search_query["field"] = search.search_by.data

    paginated_jockeys = jockeys.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )
    return paginated_jockeys


@jockey_amazon_bp.route("/", methods=["GET"])
@check_user_permissions(permissions_required=["jockey_amazon_index"])
@inject
def get_jockeys():
    search = JockeyAmazonSearchForm(request.args)
    paginated_jockeys_and_amazons = search_jockeys(
        search=search, need_archive=False
    )

    return render_template(
        "./jockey_amazon/jockeys_amazons.html",
        jockeys=paginated_jockeys_and_amazons,
        jockey_amazon_information=jockey_amazon_information,
        search_form=search,
    )

@jockey_amazon_bp.route("/archivados", methods=["GET"])
@check_user_permissions(permissions_required=["jockey_amazon_index"])
def get_deleted_jockeys():

    search = JockeyAmazonSearchForm(request.args)


    paginated_jockeys_and_amazons = search_jockeys(
        search=search, need_archive=True
    )

    return render_template(
        "./jockey_amazon/jockeys_amazons_archived.html",
        jockeys=paginated_jockeys_and_amazons,
        jockey_amazon_information=jockey_amazon_information,
        search_form=search,
    )


@jockey_amazon_bp.route("/<int:jockey_id>")
@check_user_permissions(permissions_required=["jockey_amazon_show"])
@inject
def show_jockey(
    jockey_id: int,
    jockeys: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    jockey = jockeys.get_by_id(jockey_id=jockey_id)
    if not jockey:
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    return render_template("./jockey_amazon/jockey_amazon.html", jockey_amazon=jockey)


@jockey_amazon_bp.route("/archivar/", methods=["POST"])
@check_user_permissions(permissions_required=["jockey_amazon_destroy"])
@inject
def archive_jockey(
    jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository]
):
    jockey_amazon_id = request.form["item_id"]
    archived = jockeys.archive(jockey_amazon_id)

    if not archived:
        flash("El Jinete/Amazona no existe o no ha podido ser archivado, intentelo nuevamente", "warning")
    else:
        flash("El Jinete/Amazona ha sido archivado correctamente", "success")
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey_amazon_id))


@jockey_amazon_bp.route("/recuperar/", methods=["POST"])
@check_user_permissions(permissions_required=["jockey_amazon_destroy"])
@inject
def recover_jockey(
    jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository]
):
    jockey_amazon_id = request.form["jockey_amazon_id"]
    recovered = jockeys.recover(jockey_amazon_id)

    if not recovered:
        flash("El Jinete/Amazona no existe o no ha podido ser recuperado, intentelo nuevamente", "warning")
    else:
        flash("El Jinete/Amazona ha sido recuperado correctamente", "success")
    return redirect(url_for("jockey_amazon_bp.show_jockey", jockey_id=jockey_amazon_id))

@jockey_amazon_bp.route("/delete/", methods=["POST"])
@inject
def delete_jockey(
    jockey_repository: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):
    jockey_id = request.form["item_id"]
    deleted = jockey_repository.delete(jockey_id)
    if not deleted:
        flash(
            "El Jockey/Amazon no ha podido ser eliminado, intentelo nuevamente",
            "danger",
        )
    else:
        flash("El Jockey/Amazon ha sido eliminado correctamente", "success")

    return redirect(url_for("jockey_amazon_bp.get_jockeys"))


@jockey_amazon_bp.route(
    "/editar/<int:jockey_id>/documentos/crear", methods=["GET", "POST"]
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def create_document(
    jockey_id: int,
    jockey_repository: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):

    jockey = jockey_repository.get_by_id(jockey_id)
    if not jockey:
        flash(f"El jockey con ID = {jockey_id} no existe", "danger")
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    create_form = JockeyAmazonAddDocumentsForm()

    if request.method == "POST":
        return add_document(jockey=Mapper.from_entity(jockey), create_form=create_form)

    return render_template(
        "./jockey_amazon/documents/create_document.html", form=create_form, jockey=jockey
    )


@inject
def add_document(
    jockey,
    create_form: JockeyAmazonAddDocumentsForm,
    jockey_repository: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):

    if not create_form.validate_on_submit():
        return render_template(
            "./jockey_amazon/documents/create_document.html", form=create_form, jockey=jockey
        )

    if create_form.upload_type.data == "file":
        uploaded_document = storage.upload_file(
            file=create_form.file.data,
            path=jockey_repository.storage_path,
            title=create_form.title.data,
        )

        if not uploaded_document:
            flash(f"No se pudo subir el archivo, inténtelo nuevamente", "danger")
            return redirect(
                url_for("jockey_amazon_bp.create_document", jockey_id=jockey["id"])
            )
    else:
        uploaded_document = FileMapper.file_from_form(create_form.data)

    jockey_repository.add_document(
        jockey_id=jockey["id"],
        document=Mapper.create_file(
            document_type=create_form.tag.data, file_information=uploaded_document
        ),
    )

    flash(
        f"El documento {uploaded_document.get('title')} se ha subido exitosamente",
        "success",
    )
    return redirect(url_for("jockey_amazon_bp.create_document", jockey_id=jockey["id"]))


@jockey_amazon_bp.route("/editar/<int:jockey_id>/documentos/", methods=["GET"])
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def edit_documents(
    jockey_id: int,
    jockey_repository: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)

    jockey = jockey_repository.get_by_id(jockey_id=jockey_id)
    if not jockey:
        flash(f"El jockey con ID = {jockey_id} no existe", "danger")
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    add_document_form = JockeyAmazonAddDocumentsForm()
    search_document_form = JockeyAmazonDocumentSearchForm(request.args)

    search_query = {}
    order_by = []
    if search_document_form.submit_search.data and search_document_form.validate():
        order_by = [
            (search_document_form.order_by.data, search_document_form.order.data)
        ]
        search_query = {
            "text": search_document_form.search_text.data,
            "field": search_document_form.search_by.data,
        }
        if search_document_form.filter_tag.data:
            search_query["filters"] = {"tag": search_document_form.filter_tag.data}

    paginated_files = jockey_repository.get_file_page(
        jockey_id=jockey_id,
        page=page,
        per_page=per_page,
        order_by=order_by,
        search_query=search_query,
    )

    return render_template(
        "./jockey_amazon/documents/update_documents.html",
        jockey=jockey,
        files=paginated_files,
        add_form=add_document_form,
        search_form=search_document_form,
        paginated_files=paginated_files,
    )


@jockey_amazon_bp.route("/editar/<int:jockey_id>/documentos/eliminar", methods=["POST"])
@inject
def delete_document(
    jockey_id: int,
    jockey_repository: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):

    document_id = int(request.form["item_id"])
    print(document_id, jockey_id)
    document = jockey_repository.get_document(jockey_id, document_id)
    print(
        [
            (document.id, document.jockey_amazon_id)
            for document in jockey_repository.get_all()
        ]
    )
    if not document.get("is_link"):
        deleted_in_bucket = storage.delete_file(document.get("path"))
        if not deleted_in_bucket:
            flash(
                "No se ha podido eliminar el documento, inténtelo nuevamente", "danger"
            )
            return redirect(
                url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey_id)
            )

    jockey_repository.delete_document(jockey_id, document_id)
    flash(
        f"El documento {document.get('title')} ha sido eliminado correctamente",
        "success",
    )

    return redirect(url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey_id))


@jockey_amazon_bp.route(
    "/editar/<int:jockey_id>/documentos/editar/<int:document_id>",
    methods=["GET", "POST"],
)
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def edit_document(
    jockey_id: int,
    document_id: int,
    jockey_repository: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
):

    jockey = Mapper.from_entity(jockey_repository.get_by_id(jockey_id=jockey_id))
    if not jockey:
        flash(f"El jockey con ID = {jockey_id} no existe", "danger")
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    document = jockey_repository.get_document(jockey_id, document_id)
    if not document:
        flash(f"El documento con ID = {document_id} no existe", "danger")
        return redirect(url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey_id))

    edit_form = JockeyAmazonAddDocumentsForm(data=FileMapper.to_form(document))
    if request.method == "POST":
        return update_document(jockey, document, edit_form)

    return render_template(
        "./jockey_amazon/documents/edit_document.html",
        jockey=jockey,
        document=document,
        form=edit_form,
    )


@inject
def update_document(
    jockey: dict,
    document: dict,
    edit_form: JockeyAmazonAddDocumentsForm,
    jockey_repository: AbstractJockeyAmazonRepository = Provide[
        Container.jockey_amazon_repository
    ],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    if not (
        edit_form.is_submitted()
        and edit_form.validate(is_file_already_uploaded=not document.get("is_link"))
    ):

        return render_template(
            "./jockey_amazon/documents/edit_document.html",
            jockey=jockey,
            document=document,
            form=edit_form,
        )

    uploaded_document = {}
    if edit_form.upload_type.data == "url":
        uploaded_document = FileMapper.file_from_form(edit_form.data)

    if edit_form.upload_type.data == "file":
        if edit_form.file.data:
            uploaded_document = storage.upload_file(
                edit_form.file.data,
                jockey_repository.storage_path,
                title=edit_form.title.data,
            )
        else:
            uploaded_document = FileMapper.file_from_form(edit_form.data)

        if not uploaded_document:
            flash("No se pudo modificar el archivo, inténtelo nuevamente", "danger")
            return redirect(
                url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey["id"])
            )

    success = jockey_repository.update_document(
        jockey_id=jockey["id"],
        document_id=document["id"],
        data=uploaded_document,
    )

    if success:
        flash(
            f"El documento {edit_form.title.data} ha sido modificado correctamente",
            "success",
        )
    else:
        flash(
            f"El documento {edit_form.title.data} no ha podido ser modificado", "danger"
        )

    return redirect(url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey["id"]))
