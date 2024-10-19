from flask import Blueprint, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide

from src.core.module.common.mappers import FileMapper
from src.core.module.jockey_amazon.forms import JockeyAmazonAddDocumentsForm, JockeyAmazonDocumentSearchForm
from src.core.module.common import AbstractStorageServices
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
from src.core.module.employee.repositories import EmployeeRepository
from src.core.module.equestrian.repositories import EquestrianRepository

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
@inject
def create_jockey(
        jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
        employees: EmployeeRepository = Provide[Container.employee_repository],
        equestrian: EquestrianRepository = Provide[Container.equestrian_repository]):
    create_form = JockeyAmazonCreateForm()

    create_form.organization_information.work_assignments.professor_or_therapist_id.choices = [(t.id, f"{t.name} {t.lastname}") for t in
                                                                      employees.get_therapist()]

    create_form.organization_information.work_assignments.conductor_id.choices = [(r.id, f"{r.name} {r.lastname}") for r in
                                                         employees.get_rider()]

    create_form.organization_information.work_assignments.track_assistant_id.choices = [(a.id, f"{a.name} {a.lastname}") for a in
                                                               employees.get_track_auxiliary()]

    create_form.organization_information.work_assignments.horse_id.choices = [(h.id, h.name) for h in equestrian.get_horses()]

    if request.method == "POST":
        return add_jockey(create_form=create_form, jockeys=jockeys)

    return render_template(
        "./jockey_amazon/create_jockey_amazon.html",
        form=create_form,
        EducationLevelEnum=EducationLevelEnum,
    )


@inject
def add_jockey(
        create_form,
        jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
        employees: EmployeeRepository = Provide[Container.employee_repository],
        equestrian: EquestrianRepository = Provide[Container.equestrian_repository]):
    
    if not create_form.validate_on_submit():
        print(create_form.data)
        print(create_form.errors)
        therapists = employees.get_therapist()
        riders = employees.get_rider()
        track_auxiliaries = employees.get_track_auxiliary()
        horses = equestrian.get_horses()
        return render_template(
            "./jockey_amazon/create_jockey_amazon.html",
            form=create_form,
            EducationLevelEnum=EducationLevelEnum,
            therapists=therapists,
            riders=riders,
            track_auxiliaries=track_auxiliaries,
            horses=horses
        )
    created_jockey = jockeys.add(Mapper.to_entity(create_form.data))
    flash("Jockey/Amazon creado con éxito!", "success")

    return redirect(
        url_for("jockey_amazon_bp.show_jockey", jockey_id=created_jockey.id)
    )


@jockey_amazon_bp.route("/<int:jockey_id>")
@check_user_permissions(permissions_required=["jockey_amazon_show"])
@inject
def show_jockey(
        jockey_id: int,
        jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    jockey = jockeys.get_by_id(jockey_id=jockey_id)
    if not jockey:
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    return render_template("./jockey_amazon/jockey_amazon.html", jockey_amazon=jockey)


@jockey_amazon_bp.route("/editar/<int:jockey_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def edit_jockey(
        jockey_id: int,
        jockeys: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    jockey = jockeys.get_by_id(jockey_id)
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
    jockey = jockeys.get_by_id(jockey_id)
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
    deleted = jockey_repository.delete(jockey_id)
    if not deleted:
        flash("El Jockey/Amazon no ha podido ser eliminado, intentelo nuevamente", "danger")
    else:
        flash("El Jockey/Amazon ha sido eliminado correctamente", "success")

    return redirect(url_for("jockey_amazon_bp.get_jockeys"))


@jockey_amazon_bp.route("/editar/<int:jockey_id>/documentos/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def create_document(jockey_id: int,
                    jockey_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository]):

    jockey = jockey_repository.get_by_id(jockey_id)
    if not jockey:
        flash(f"El jockey con ID = {jockey_id} no existe", "danger")
        return redirect(url_for("jockey_amazon_bp.get_jockeys"))

    jockey = Mapper.from_entity(jockey)
    create_form = JockeyAmazonAddDocumentsForm()

    if request.method == "POST":
        return add_document(jockey=jockey, create_form=create_form)

    return render_template("./jockey_amazon/create_document.html", form=create_form, jockey=jockey)


@inject
def add_document(jockey,
                 create_form: JockeyAmazonAddDocumentsForm,
                 jockey_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
                 storage: AbstractStorageServices = Provide[Container.storage_services]):

    if not create_form.validate_on_submit():
        print(create_form.errors)
        print(create_form.data)
        return render_template("./jockey_amazon/create_document.html", form=create_form, jockey=jockey)

    if create_form.upload_type.data == "file":
        uploaded_document = storage.upload_file(
            file=create_form.file.data, path=jockey_repository.storage_path, title=create_form.title.data)

        if not uploaded_document:
            flash(f"No se pudo subir el archivo, inténtelo nuevamente", "danger")
            return redirect(url_for("jockey_amazon_bp.create_document", jockey_id=jockey["id"]))
    else:
        uploaded_document = FileMapper.file_from_form(create_form.data)

    jockey_repository.add_document(
        jockey_id=jockey["id"],
        document=Mapper.create_file(
            document_type=create_form.tag.data, file_information=uploaded_document
        ))

    flash(f"El documento {uploaded_document.get('title')} se ha subido exitosamente", "success")
    return redirect(url_for("jockey_amazon_bp.create_document", jockey_id=jockey["id"]))


@jockey_amazon_bp.route("/editar/<int:jockey_id>/documentos/", methods=["GET"])
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def edit_documents(
        jockey_id: int,
        jockey_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
        storage: AbstractStorageServices = Provide[Container.storage_services]):
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
        order_by = [(search_document_form.order_by.data, search_document_form.order.data)]
        search_query = {
            "text": search_document_form.search_text.data,
            "field": search_document_form.search_by.data,
        }
        if search_document_form.filter_tag.data:
            search_query["filters"] = {"tag": search_document_form.filter_tag.data}

    paginated_files = jockey_repository.get_file_page(
        jockey_id=jockey_id, page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )

    return render_template(
        "./jockey_amazon/update_documents.html",
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
        jockey_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
        storage: AbstractStorageServices = Provide[Container.storage_services]):

    document_id = int(request.form["item_id"])
    print(document_id, jockey_id)
    document = jockey_repository.get_document(jockey_id, document_id)
    print([(document.id, document.jockey_amazon_id) for document in jockey_repository.get_all()])
    if not document.get("is_link"):
        deleted_in_bucket = storage.delete_file(document.get("path"))
        if not deleted_in_bucket:
            flash("No se ha podido eliminar el documento, inténtelo nuevamente", "danger")
            return redirect(url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey_id))

    jockey_repository.delete_document(jockey_id, document_id)
    flash(f"El documento {document.get('title')} ha sido eliminado correctamente", "success")

    return redirect(url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey_id))


@jockey_amazon_bp.route("/editar/<int:jockey_id>/documentos/editar/<int:document_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["jockey_amazon_update"])
@inject
def edit_document(
        jockey_id: int,
        document_id: int,
        jockey_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository]):

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
        "./jockey_amazon/edit_document.html",
        jockey=jockey,
        document=document,
        form=edit_form,
    )


@inject
def update_document(jockey: dict,
                    document: dict,
                    edit_form: JockeyAmazonAddDocumentsForm,
                    jockey_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
                    storage: AbstractStorageServices = Provide[Container.storage_services]):
    if not (edit_form.is_submitted()
            and
            edit_form.validate(is_file_already_uploaded=not document.get("is_link"))):

        return render_template(
            "./jockey_amazon/edit_document.html",
            jockey=jockey,
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
                jockey_repository.storage_path,
                title=edit_form.title.data
            )
        else:
            uploaded_document = FileMapper.file_from_form(edit_form.data)

        if not uploaded_document:
            flash("No se pudo modificar el archivo, inténtelo nuevamente", "danger")
            return redirect(url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey["id"]))

    success = jockey_repository.update_document(
        jockey_id=jockey["id"],
        document_id=document["id"],
        data=uploaded_document,
    )

    if success:
        flash(f"El documento {edit_form.title.data} ha sido modificado correctamente", "success")
    else:
        flash(f"El documento {edit_form.title.data} no ha podido ser modificado", "danger")

    return redirect(url_for("jockey_amazon_bp.edit_documents", jockey_id=jockey["id"]))
