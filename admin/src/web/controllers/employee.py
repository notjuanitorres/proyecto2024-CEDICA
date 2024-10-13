from flask import Blueprint, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.employee.forms import EmployeeSearchForm
from src.core.module.employee import (
    EmployeeMapper as Mapper,
    AbstractEmployeeServices,
    EmployeeCreateForm,
    EmployeeEditForm,
    EmployeeAddDocumentsForm,
    employment_enums as employment_information,
)
from src.core.module.common import AbstractStorageServices


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
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
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
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    if not create_form.validate_on_submit():
        return render_template("./employee/create_employee.html", form=create_form)

    documents = create_form.documents.data

    uploaded_documents = [
        ("DNI", storage.upload_batch(documents.get("dni"), employees.storage_path)),
        ("TITLE", storage.upload_batch(documents.get("title"), employees.storage_path)),
        (
            "CURRICULUM_VITAE",
            [
                storage.upload_file(
                    documents.get("curriculum_vitae"), employees.storage_path
                )
            ],
        ),
    ]

    created_employee = employees.create_employee(
        employee=Mapper.to_entity(create_form.data, uploaded_documents),
    )

    flash("Miembro creado con exito!", "success")

    return redirect(
        url_for("employee_bp.show_employee", employee_id=created_employee["id"])
    )


@employee_bp.route("/<int:employee_id>")
@check_user_permissions(permissions_required=["equipo_show"])
@inject
def show_employee(
    employee_id: int,
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
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
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
):
    employee = employees.get_employee(employee_id)
    if not employee:
        return redirect(url_for("employee_bp.get_employees"))

    update_form = EmployeeEditForm(
        data=employee,
        id=employee_id,
        # TODO: This lines could be passed as a hidden field on the form
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
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
):
    employee = employees.get_employee(employee_id)
    if not update_form.validate_on_submit():
        return render_template(
            "./employee/update_employee.html", form=update_form, employee=employee
        )

    if not employees.update_employee(employee_id, Mapper.flat_form(update_form.data)):
        flash("No se ha podido actualizar al miembro del equipo", "warning")
        return render_template("./employee/update_employee.html")

    flash("El miembro del equipo ha sido actualizado exitosamente ")
    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))


@employee_bp.route("/delete/", methods=["POST"])
@inject
def delete_employee(employee_services: AbstractEmployeeServices = Provide[Container.employee_services]):
    employee_id = request.form["item_id"]
    deleted = employee_services.delete_employee(employee_id)
    if not deleted:
        flash("El empleado no ha podido ser eliminado, intentelo nuevamente", "danger")
    else:
        flash("El empleado ha sido eliminado correctamente", "success")

    return redirect(url_for("employee_bp.get_employees"))


@employee_bp.route("/editar/<int:employee_id>/documentos/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def edit_documents(
    employee_id: int,
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    add_document_form = EmployeeAddDocumentsForm()
    employee = employees.get_employee(employee_id=employee_id)
    documents = [
        {"file": file, "url": storage.presigned_download_url(file.get("filename"))}
        for file in employee.get("files")
    ]

    if request.method == "POST":
        return update_documents(add_document_form, employee, documents)

    return render_template(
        "./employee/update_documents.html",
        employee=employee,
        documents=documents,
        add_form=add_document_form,
    )


@inject
def update_documents(
    add_form: EmployeeAddDocumentsForm,
    employee: dict,
    documents: list[dict],
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    if not add_form.validate_on_submit():
        return render_template(
            "./employee/update_documents.html",
            add_form=add_form,
            employee=employee,
            documents=documents,
        )
    employee_id = employee["id"]
    uploaded_document = storage.upload_file(
        file=add_form.file.data, path=employees.storage_path
    )
    employees.add_document(
        employee_id=employee_id,
        document=Mapper.create_file(
            document_type=add_form.tag.data, file_information=uploaded_document
        ),
    )

    return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))


@employee_bp.route("/editar/<int:employee_id>/documentos/eliminar", methods=["POST"])
@inject
def delete_document(
    employee_id: int,
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    document_id = request.form["item_id"]
    document = employees.get_document(employee_id, document_id)
    
    storage.delete_file(document.get("filename"))
    employees.delete_document(employee_id, document_id)

    flash(f"El documento {document.get("original_filename")} ha sido eliminado correctamente", "success")
    return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))