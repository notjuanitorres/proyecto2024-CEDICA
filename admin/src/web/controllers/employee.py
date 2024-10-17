from typing import Dict

from flask import Blueprint, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.employee import (
    EmployeeMapper,
    AbstractEmployeeRepository,
    EmployeeCreateForm,
    EmployeeEditForm,
    EmployeeSearchForm,
    EmployeeAddDocumentsForm,
    EmployeeDocumentSearchForm,
    employment_enums as employment_information,
)
from src.core.module.common import AbstractStorageServices, FileMapper


employee_bp = Blueprint(
    "employee_bp",
    __name__,
    template_folder="./templates/employee/",
    url_prefix="/equipo/",
)


@employee_bp.route("/", methods=["GET"])
@check_user_permissions(permissions_required=["equipo_index"])
@inject
def get_employees(
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    search = EmployeeSearchForm(request.args)
    search_query = {}
    order_by = []

    if search.submit_search.data and search.validate():
        order_by = [(search.order_by.data, search.order.data)]
        search_query = {
            "text": search.search_text.data,
            "field": search.search_by.data,
        }
        if search.filter_job_position.data:
            search_query["filters"] = {"position": search.filter_job_position.data}

    paginated_employees = employees.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )

    return render_template(
        "./employee/employees.html",
        employees=paginated_employees,
        employment_information=employment_information,
        search_form=search,
    )


@employee_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_new"])
def create_employee():
    create_form = EmployeeCreateForm()

    if request.method == "POST":
        return add_employee(create_form=create_form)

    return render_template("./employee/create_employee.html", form=create_form)


@inject
def add_employee(
    create_form,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    if not create_form.validate_on_submit():
        return render_template("./employee/create_employee.html", form=create_form)

    created_employee = employees.add(
        employee=EmployeeMapper.to_entity(create_form.data, []),
    )

    flash("Miembro creado con exito!", "success")

    return redirect(
        url_for("employee_bp.create_document", employee_id=created_employee["id"])
    )


@employee_bp.route("/editar/<int:employee_id>/documentos/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def create_document(employee_id: int,
                    employees: AbstractEmployeeRepository = Provide[Container.employee_repository]):

    employee = employees.get_employee(employee_id, documents=False)
    if not employee:
        flash(f"El empleado con ID = {employee_id} no existe", "danger")
        return redirect(url_for("employee_bp.get_employees"))

    create_form = EmployeeAddDocumentsForm()
    if request.method == "POST":
        return add_document(employee=employee, create_form=create_form)

    return render_template("./employee/create_document.html", form=create_form, employee=employee)


@inject
def add_document(employee,
                 create_form: EmployeeAddDocumentsForm,
                 employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
                 storage: AbstractStorageServices = Provide[Container.storage_services],
                 ):

    if not create_form.validate_on_submit():
        return render_template("./employee/create_document.html", form=create_form, employee=employee)

    if create_form.upload_type.data == "file":
        uploaded_document = storage.upload_file(
            file=create_form.file.data, path=employees.storage_path, title=create_form.title.data)

        if not uploaded_document:
            flash(f"No se pudo subir el archivo, inténtelo nuevamente", "danger")
            return redirect(url_for("employee_bp.create_document", employee_id=employee["id"]))
    else:
        uploaded_document = FileMapper.file_from_form(create_form.data)

    employees.add_document(
        employee_id=employee["id"],
        document=EmployeeMapper.create_file(
            document_type=create_form.tag.data, file_information=uploaded_document
        ))

    flash(f"El documento {uploaded_document.get('title')} se ha subido exitosamente", "success")
    return redirect(url_for("employee_bp.create_document", employee_id=employee["id"]))


@employee_bp.route("/<int:employee_id>")
@check_user_permissions(permissions_required=["equipo_show"])
@inject
def show_employee(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    employee = employees.get_employee(employee_id=employee_id)
    if not employee:
        return redirect(url_for("employee_bp.get_employees"))

    return render_template("./employee/employee.html", employee=employee)


@employee_bp.route("/editar/<int:employee_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def edit_employee(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    employee = employees.get_employee(employee_id)
    if not employee:
        return redirect(url_for("employee_bp.get_employees"))

    update_form = EmployeeEditForm(
        data=employee,
        id=employee_id,
        current_email=employee["email"],
        current_dni=employee["dni"],
    )

    if request.method == "POST":
        return update_employee(update_form=update_form, employee_id=employee_id)

    return render_template(
        "./employee/update_employee.html", form=update_form, employee=employee
    )


@inject
def update_employee(
    employee_id: int,
    update_form,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    employee = employees.get_employee(employee_id)
    if not update_form.validate_on_submit():
        return render_template(
            "./employee/update_employee.html", form=update_form, employee=employee
        )

    if not employees.update(employee_id, EmployeeMapper.flat_form(update_form.data)):
        flash("No se ha podido actualizar al miembro del equipo", "warning")
        return render_template("./employee/update_employee.html")

    flash("El miembro del equipo ha sido actualizado exitosamente ")
    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))


@employee_bp.route("/delete/", methods=["POST"])
@inject
def delete_employee(employee_repository: AbstractEmployeeRepository = Provide[Container.employee_repository]):
    employee_id = request.form["item_id"]
    deleted = employee_repository.delete_employee(employee_id)
    if not deleted:
        flash("El empleado no ha podido ser eliminado, intentelo nuevamente", "danger")
    else:
        flash("El empleado ha sido eliminado correctamente", "success")

    return redirect(url_for("employee_bp.get_employees"))


@employee_bp.route("/editar/<int:employee_id>/documentos/", methods=["GET"])
@check_user_permissions(permissions_required=["employee_update"])
@inject
def edit_documents(
    employee_id: int,
    employee_repository: AbstractEmployeeRepository = Provide[Container.employee_repository],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)

    employee = employee_repository.get_employee(employee_id=employee_id, documents=False)
    if not employee:
        flash(f"El empleado con ID = {employee_id} no existe", "danger")
        return redirect(url_for("employee_bp.get_employees"))

    add_document_form = EmployeeAddDocumentsForm()
    search_document_form = EmployeeDocumentSearchForm(request.args)

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

    paginated_files = employee_repository.get_file_page(
        employee_id=employee_id, page=page, per_page=per_page, order_by=order_by, search_query=search_query
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
        "./employee/update_documents.html",
        employee=employee,
        documents=documents,
        add_form=add_document_form,
        search_form=search_document_form,
        paginated_files=paginated_files,
    )


@inject
def update_documents(
    add_form: EmployeeAddDocumentsForm,
    search_form: EmployeeDocumentSearchForm,
    employee: dict,
    documents: list[dict],
    paginated_files,
    employee_repository: AbstractEmployeeRepository = Provide[Container.employee_repository],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    if not add_form.validate_on_submit():
        return render_template(
            "./employee/update_documents.html",
            add_form=add_form,
            employee=employee,
            documents=documents,
            search_form=search_form,
            paginated_files=paginated_files,
        )

    employee_id = employee["id"]
    if add_form.upload_type.data == 'file':
        uploaded_document = storage.upload_file(
            file=add_form.file.data, path=employee_repository.storage_path, title=add_form.title.data
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
        return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))

    employee_repository.add_document(
        employee_id=employee_id,
        document=EmployeeMapper.create_file(
            document_type=add_form.tag.data, file_information=uploaded_document
        ),
    )
    flash(f"El documento {uploaded_document.get('title')} se ha subido exitosamente", "success")
    return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))


@employee_bp.route("/editar/<int:employee_id>/documentos/eliminar", methods=["POST"])
@inject
def delete_document(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    document_id = int(request.form["item_id"])
    document = employees.get_document(employee_id, document_id)

    if not document.get("is_link"):
        deleted_in_bucket = storage.delete_file(document.get("path"))
        if not deleted_in_bucket:
            flash("No se ha podido eliminar el documento, inténtelo nuevamente", "danger")
            return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))

    employees.delete_document(employee_id, document_id)
    flash(f"El documento {document.get("title")} ha sido eliminado correctamente", "success")
    
    return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))


@employee_bp.route("/editar/<int:employee_id>/documentos/editar/<int:document_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def edit_document(
    employee_id: int,
    document_id: int,
    employee_repository: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    employee = employee_repository.get_employee(employee_id=employee_id, documents=False)
    if not employee:
        flash(f"El empleado con ID = {employee_id} no existe", "danger")
        return redirect(url_for("employee_bp.get_employees"))

    document = employee_repository.get_document(employee_id, document_id)
    if not document:
        flash(f"El documento con ID = {document_id} no existe", "danger")
        return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))

    edit_form = EmployeeAddDocumentsForm(data=FileMapper.to_form(document))
    if request.method == "POST":
        return update_document(employee, document, edit_form)

    return render_template(
        "./employee/edit_document.html",
        employee=employee,
        document=document,
        form=edit_form,
    )


@inject
def update_document(employee: dict,
                    document: dict,
                    edit_form: EmployeeAddDocumentsForm,
                    employee_repository: AbstractEmployeeRepository = Provide[Container.employee_repository],
                    storage: AbstractStorageServices = Provide[Container.storage_services],):

    if not (edit_form.is_submitted()
            and
            edit_form.validate(is_file_already_uploaded=not document.get("is_link"))):

        return render_template(
            "./employee/edit_document.html",
            employee=employee,
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
                employee_repository.storage_path,
                title=edit_form.title.data
            )
        else:
            uploaded_document = FileMapper.file_from_form(edit_form.data)

        if not uploaded_document:
            flash("No se pudo modificar el archivo, inténtelo nuevamente", "danger")
            return redirect(url_for("employee_bp.edit_documents", employee_id=employee["id"]))

    success = employee_repository.update_document(
        employee_id=employee["id"],
        document_id=document["id"],
        data=uploaded_document,
    )

    if success:
        flash(f"El documento {edit_form.title.data} ha sido modificado correctamente", "success")
    else:
        flash(f"El documento {edit_form.title.data} no ha podido ser modificado", "danger")

    return redirect(url_for("employee_bp.edit_documents", employee_id=employee["id"]))
