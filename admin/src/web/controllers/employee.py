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
from src.core.module.user import (
    AbstractUserRepository,
    AccountSearchForm,
    AccountSelectForm,
)


employee_bp = Blueprint(
    "employee_bp",
    __name__,
    template_folder="../templates/employee/",
    url_prefix="/equipo/",
)


@inject
def search_employees(
    search: EmployeeSearchForm,
    need_archive: bool,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Helper function to search employees.

    Args:
        search (EmployeeSearchForm): The form for searching employees.
        need_archived (bool): Indicates if the search should include archived employees.
        equestrian_repository (AbstractEmployeeRepository): The employee repository.

    Returns:
        Pagination: The paginated list of employees.
    """
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

        if search.filter_job_position.data:
            search_query["filters"]["position"] = search.filter_job_position.data
        if search.filter_is_active.data:
            search_query["filters"]["is_active"] = search.filter_is_active.data

    paginated_employees = employees.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )
    return paginated_employees


@employee_bp.route("/", methods=["GET"])
@check_user_permissions(permissions_required=["equipo_index"])
def get_employees():
    """
    Retrieve and display a paginated list of active employees.

    Returns:
        rendered template: The employees.html template with:
            - paginated employee list
            - employment information
            - search form
    """
    search_form = EmployeeSearchForm(request.args)

    paginated_employees = search_employees(search=search_form, need_archive=False)

    return render_template(
        "./employee/list/employees.html",
        employees=paginated_employees,
        employment_information=employment_information,
        search_form=search_form,
    )


@employee_bp.route("/archivados", methods=["GET"])
@check_user_permissions(permissions_required=["equipo_index"])
def get_deleted_employees():
    """
    Retrieve and display a paginated list of archived employees.

    Returns:
        rendered template: The employees_archived.html template with:
            - paginated archived employee list
            - employment information
            - search form
    """
    search_form = EmployeeSearchForm(request.args)
    paginated_employees = search_employees(search=search_form, need_archive=True)
    return render_template(
        "./employee/list/employees_archived.html",
        employees=paginated_employees,
        employment_information=employment_information,
        search_form=search_form,
    )


@employee_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_new"])
def create_employee():
    """
    Handle the creation of a new employee.

    Returns:
        GET: rendered template: The create_employee.html template with the creation form
        POST: redirect: To the document creation page for the new employee
    """
    create_form = EmployeeCreateForm()

    if request.method == "POST":
        return add_employee(create_form=create_form)

    return render_template("./employee/create/create_employee.html", form=create_form)


@inject
def add_employee(
    create_form,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Process the employee creation form and add a new employee to the system.

    Returns:
        - A redirect to the document creation page on success
        - The rendered create_employee template on validation failure
    """
    if not create_form.validate_on_submit():
        return render_template("./employee/create/create_employee.html", form=create_form)

    created_employee = employees.add(
        employee=EmployeeMapper.to_entity(create_form.data, []),
    )

    flash("Miembro creado con exito!", "success")
    return redirect(
        url_for("employee_bp.create_document", employee_id=created_employee["id"])
    )


@employee_bp.route(
    "/editar/<int:employee_id>/documentos/crear", methods=["GET", "POST"]
)
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def create_document(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Handle document creation for a specific employee.

    Args:
        employee_id (int): The ID of the employee to add documents for
        employees (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        - A redirect to employees list if employee doesn't exist
        - The rendered create_document template with form and employee data
    """
    employee = employees.get_employee(employee_id, documents=False)
    if not employee:
        flash(f"El empleado con ID = {employee_id} no existe", "danger")
        return redirect(url_for("employee_bp.get_employees"))

    create_form = EmployeeAddDocumentsForm()
    if request.method == "POST":
        return add_document(employee=employee, create_form=create_form)

    return render_template(
        "./employee/create/create_document.html", form=create_form, employee=employee
    )


@inject
def add_document(
    employee,
    create_form: EmployeeAddDocumentsForm,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    """
    Process the document creation form and add a new document to an employee's profile.

    Args:
        employee (dict): The employee's information
        create_form (EmployeeAddDocumentsForm): The validated form containing document data
        employees (AbstractEmployeeRepository): Repository for employee operations
        storage (AbstractStorageServices): Service for handling file storage

    Returns:
        - A redirect to document creation page on success
        - The rendered create_document template on validation failure
    """
    if not create_form.validate_on_submit():
        return render_template(
            "./employee/create/create_document.html", form=create_form, employee=employee
        )

    if create_form.upload_type.data == "file":
        uploaded_document = storage.upload_file(
            file=create_form.file.data,
            path=employees.storage_path,
            title=create_form.title.data,
        )

        if not uploaded_document:
            flash("No se pudo subir el archivo, inténtelo nuevamente", "danger")
            return redirect(
                url_for("employee_bp.create_document", employee_id=employee["id"])
            )
    else:
        uploaded_document = FileMapper.file_from_form(create_form.data)

    employees.add_document(
        employee_id=employee["id"],
        document=EmployeeMapper.create_file(
            document_type=create_form.tag.data, file_information=uploaded_document
        ),
    )

    flash(
        f"El documento {uploaded_document.get('title')} se ha subido exitosamente",
        "success",
    )
    return redirect(url_for("employee_bp.create_document", employee_id=employee["id"]))


@employee_bp.route("/<int:employee_id>")
@check_user_permissions(permissions_required=["equipo_show"])
@inject
def show_employee(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
    accounts: AbstractUserRepository = Provide[Container.user_repository],
):
    """
    Display detailed information about a specific employee.

    Args:
        employee_id (int): The ID of the employee to display
        employees (AbstractEmployeeRepository): Repository for employee operations
        accounts (AbstractUserRepository): Repository for user account operations
    
    Returns:
        - A redirect to employees list if employee doesn't exist
        - The rendered employee template with employee and account data
    """

    employee = employees.get_employee(employee_id=employee_id)
    employee_account = accounts.get_user(employee.get("user_id"))
    if not employee:
        return redirect(url_for("employee_bp.get_employees"))

    return render_template("./employee/employee.html", employee=employee, account=employee_account)


@employee_bp.route("/editar/<int:employee_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def edit_employee(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Handle employee information updates.

    Args:
        employee_id (int): The ID of the employee to edit
        employees (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        - A redirect to employees list if employee doesn't exist
        - A redirect to employee view if employee is archived
        - The rendered update_employee template with form and employee data
    """
    employee = employees.get_employee(employee_id)
    if not employee:
        flash("El empleado solicitado no existe", "danger")
        return redirect(url_for("employee_bp.get_employees"))

    if employee.get("is_deleted"):
        flash("No se puede editar un empleado archivado", "warning")
        return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))

    update_form = EmployeeEditForm(
        data=employee,
        id=employee_id,
        current_email=employee["email"],
        current_dni=employee["dni"],
    )

    if request.method == "POST":
        return update_employee(update_form=update_form, employee_id=employee_id)

    return render_template(
        "./employee/update/update_employee.html", form=update_form, employee=employee
    )


@inject
def update_employee(
    employee_id: int,
    update_form,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Process the employee update form and save changes to the employee's information.

    Args:
        employee_id (int): The ID of the employee to update
        update_form (EmployeeEditForm): The validated form containing updated employee data
        employees (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        - A redirect to employee view page on success
        - The rendered update_employee template on validation failure
    """

    employee = employees.get_employee(employee_id)
    if not update_form.validate_on_submit():
        return render_template(
            "./employee/update/update_employee.html", form=update_form, employee=employee
        )

    if not employees.update(employee_id, EmployeeMapper.flat_form(update_form.data)):
        flash("No se ha podido actualizar al miembro del equipo", "warning")
        return render_template("./employee/update/update_employee.html")

    flash("El miembro del equipo ha sido actualizado exitosamente ")
    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))


@employee_bp.route("/archivar/", methods=["POST"])
@check_user_permissions(permissions_required=["equipo_destroy"])
@inject
def archive_employee(
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Archive an employee record.

    Args:
        employees (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        Response: A redirect to the employee view page with success/failure message
    """
    employee_id = request.form["item_id"]
    archived = employees.archive(employee_id)

    if not archived:
        flash("El miembro del equipo no existe o no puede ser archivado", "warning")
    else:
        flash("El miembro del equipo ha sido archivado correctamente", "success")
    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))


@employee_bp.route("/recuperar/", methods=["POST"])
@check_user_permissions(permissions_required=["equipo_destroy"])
@inject
def recover_employee(
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Recover an archived employee record.

    Args:
        employees (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        Response: A redirect to the employee view page with success/failure message
    """

    employee_id = request.form["employee_id"]
    recovered = employees.recover(employee_id)

    if not recovered:
        flash("El miembro del equipo no existe o no puede ser recuperado", "warning")
    else:
        flash("El miembro del equipo ha sido recuperado correctamente", "success")
    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))


@employee_bp.route("/eliminar/", methods=["POST"])
@check_user_permissions(permissions_required=["equipo_destroy"])
@inject
def delete_employee(
    employee_repository: AbstractEmployeeRepository = Provide[
        Container.employee_repository
    ],
):
    """
    Permanently delete an employee record.

    Args:
        employee_repository (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        Response: A redirect to the employees list with success/failure message
    """

    employee_id = request.form["item_id"]
    try:
        employee_id = int(employee_id)
    except ValueError:
        flash("El ID del empleado no es valido", "danger")
        return redirect(url_for("employee_bp.get_employees"))

    conflicts = employee_repository.count_id_in_charges_and_payments(employee_id)
    if conflicts:
        flash(
            f"El empleado no puede ser eliminado ya que está presente en {conflicts} pagos y/o cobros",
            "danger",
        )
        return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))

    deleted = employee_repository.delete(employee_id)
    if not deleted:
        flash("El empleado no ha podido ser eliminado, intentelo nuevamente", "danger")
    else:
        flash("El empleado ha sido eliminado correctamente", "success")

    return redirect(url_for("employee_bp.get_employees"))


@employee_bp.route("/sincronizar-cuenta/<int:employee_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def link_account(
    employee_id: int,
    page: int = 1,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
    users: AbstractUserRepository = Provide[Container.user_repository],
):
    """
    Handle linking a user account to an employee profile.

    This endpoint supports both GET and POST methods:
    - GET: Display the account selection form
    - POST: Process the account linking

    Args:
        employee_id (int): The ID of the employee to link an account to
        page (int): The current page number for pagination
        employees (AbstractEmployeeRepository): Repository for employee operations
        users (AbstractUserRepository): Repository for user account operations

    Returns:
        - employee data
        - paginated accounts list
        - search and selection forms
    """
    employee = employees.get_employee(employee_id)
    if not employee:
        flash(f"El empleado solicitado no existe", "danger")
        return redirect(url_for("employee_bp.get_employees"))

    page = request.args.get("page", type=int, default=1)
    search_account = AccountSearchForm(request.args)
    select_account = AccountSelectForm()

    if request.method == "GET" and search_account.validate():
        accounts = users.get_active_users(
            page=page, search=search_account.search_text.data
        )
    else:
        accounts = users.get_active_users(page=page)

    if request.method == "POST":
        return set_employee_account(employee, search_account, select_account, accounts)

    return render_template(
        "./employee/update/update_account.html",
        employee=employee,
        accounts=accounts,
        search_form=search_account,
        select_form=select_account,
    )


@inject
def set_employee_account(
    employee,
    search_form,
    select_form,
    active_accounts,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Process the account linking form and associate a user account with an employee.

    Args:
        employee (dict): The employee's information
        search_form (AccountSearchForm): Form for searching accounts
        select_form (AccountSelectForm): Form for selecting an account
        active_accounts (list): List of active user accounts
        employees (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        - A redirect to employee view page on success
        - The rendered update_account template on validation failure
    """
    if not (select_form.submit_item.data and select_form.validate()):
        return render_template(
            "./employee/update/update_account.html",
            employee=employee,
            accounts=active_accounts,
            search_form=search_form,
            select_form=select_form,
        )
    employee_id = employee.get("id")
    account_id = select_form.selected_item.data

    employees.link_account(employee_id, account_id)

    flash(
        f"Se ha asociado correctamente a {employee.get("name")} con su cuenta",
        "success",
    )
    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))


@employee_bp.route("/quitar-cuenta/<int:employee_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def unlink_account(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Remove the association between an employee and their user account.

    Args:
        employee_id (int): The ID of the employee to unlink
        employees (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        Response: A redirect to the employee view page with success message
    """

    employee = employees.get_employee(employee_id)
    employees.link_account(employee_id, None)

    flash(
        f"Se ha desasociado correctamente a {employee.get("name")} de su cuenta",
        "warning",
    )
    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))


@employee_bp.route("/editar/<int:employee_id>/documentos/", methods=["GET"])
@check_user_permissions(permissions_required=["equipo_show"])
@inject
def edit_documents(
    employee_id: int,
    employee_repository: AbstractEmployeeRepository = Provide[
        Container.employee_repository
    ],
):
    """
    Display and manage documents associated with an employee.

    Args:
        employee_id (int): The ID of the employee whose documents to edit
        employee_repository (AbstractEmployeeRepository): Repository for employee operations

    Returns:
        - A redirect to employees list if employee doesn't exist
        - The rendered update_documents template with:
            - employee data
            - paginated files list
            - document forms
    """
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)

    employee = employee_repository.get_employee(
        employee_id=employee_id, documents=False
    )
    if not employee:
        flash(f"El empleado con ID = {employee_id} no existe", "danger")
        return redirect(url_for("employee_bp.get_employees"))

    add_document_form = EmployeeAddDocumentsForm()
    search_document_form = EmployeeDocumentSearchForm(request.args)

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

    paginated_files = employee_repository.get_file_page(
        employee_id=employee_id,
        page=page,
        per_page=per_page,
        order_by=order_by,
        search_query=search_query,
    )

    return render_template(
        "./employee/update/update_documents.html",
        employee=employee,
        files=paginated_files,
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
    employee_repository: AbstractEmployeeRepository = Provide[
        Container.employee_repository
    ],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    """
    Process document updates for an employee.

    Args:
        add_form (EmployeeAddDocumentsForm): Form for adding new documents
        search_form (EmployeeDocumentSearchForm): Form for searching documents
        employee (dict): The employee's information
        documents (list): List of employee's documents
        paginated_files: Pagination object for documents
        employee_repository (AbstractEmployeeRepository): Repository for employee operations
        storage (AbstractStorageServices): Service for handling file storage

    Returns:
        - A redirect to documents edit page on success
        - The rendered update_documents template on validation failure
    """

    if not add_form.validate_on_submit():
        return render_template(
            "./employee/update/update_documents.html",
            add_form=add_form,
            employee=employee,
            documents=documents,
            search_form=search_form,
            paginated_files=paginated_files,
        )

    employee_id = employee["id"]
    if add_form.upload_type.data == "file":
        uploaded_document = storage.upload_file(
            file=add_form.file.data,
            path=employee_repository.storage_path,
            title=add_form.title.data,
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
    flash(
        f"El documento {uploaded_document.get('title')} se ha subido exitosamente",
        "success",
    )
    return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))


@employee_bp.route("/editar/<int:employee_id>/documentos/eliminar", methods=["POST"])
@inject
def delete_document(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    """
    Delete a document associated with an employee.

    Args:
        employee_id (int): The ID of the employee whose document to delete
        employees (AbstractEmployeeRepository): Repository for employee operations
        storage (AbstractStorageServices): Service for handling file storage

    Returns:
        Response: A redirect to the documents edit page with success/failure message
    """

    document_id = int(request.form["item_id"])
    document = employees.get_document(employee_id, document_id)

    if not document.get("is_link"):
        deleted_in_bucket = storage.delete_file(document.get("path"))
        if not deleted_in_bucket:
            flash(
                "No se ha podido eliminar el documento, inténtelo nuevamente", "danger"
            )
            return redirect(
                url_for("employee_bp.edit_documents", employee_id=employee_id)
            )

    employees.delete_document(employee_id, document_id)
    flash(
        f"El documento {document.get("title")} ha sido eliminado correctamente",
        "success",
    )

    return redirect(url_for("employee_bp.edit_documents", employee_id=employee_id))


@employee_bp.route("/toggle-activation/<int:employee_id>")
@inject
def toggle_activation(
    employee_id: int,
    employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
    users: AbstractUserRepository = Provide[Container.user_repository],
):
    """
    Toggle the active status of an employee and their associated user account.

    Args:
        employee_id (int): The ID of the employee to toggle
        employees (AbstractEmployeeRepository): Repository for employee operations
        users (AbstractUserRepository): Repository for user account operations

    Returns:
        Response: A redirect to the previous page or home with success message
    """
    employee = employees.get_employee(employee_id)
    account = employee.get("user_id")
    is_active = employees.toggled_activation(employee_id)
    if account:
        if is_active and not users.is_user_enabled(account):
            users.toggle_activation(account)
        elif not is_active and users.is_user_enabled(account):
            users.toggle_activation(account)
    flash("La operacion fue un exito", "success")
    return redirect(request.referrer or url_for("index_bp.home"))


@employee_bp.route(
    "/editar/<int:employee_id>/documentos/editar/<int:document_id>",
    methods=["GET", "POST"],
)
@check_user_permissions(permissions_required=["equipo_update"])
@inject
def edit_document(
    employee_id: int,
    document_id: int,
    employee_repository: AbstractEmployeeRepository = Provide[
        Container.employee_repository
    ],
):
    """
    Handle editing of a specific document.

    This endpoint supports both GET and POST methods:
    - GET: Display the document edit form
    - POST: Process the document update

    Args:
        employee_id (int): The ID of the employee whose document to edit
        document_id (int): The ID of the document to edit
        employee_repository (AbstractEmployeeRepository): Repository for employee operations
    Returns:
        - A redirect if employee or document doesn't exist
        - The rendered edit_document template with form and data
    """

    employee = employee_repository.get_employee(
        employee_id=employee_id, documents=False
    )
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
        "./employee/update/edit_document.html",
        employee=employee,
        document=document,
        form=edit_form,
    )


@inject
def update_document(
    employee: dict,
    document: dict,
    edit_form: EmployeeAddDocumentsForm,
    employee_repository: AbstractEmployeeRepository = Provide[
        Container.employee_repository
    ],
    storage: AbstractStorageServices = Provide[Container.storage_services],
):
    """
    Process document edit form and update the document.

    Args:
        employee (dict): The employee's information
        document (dict): The current document information
        edit_form (EmployeeAddDocumentsForm): The validated form containing updated document data
        employee_repository (AbstractEmployeeRepository): Repository for employee operations
        storage (AbstractStorageServices): Service for handling file storage

    Returns:
        Union[Response, str]: Either:
            - A redirect to documents edit page on success
            - The rendered edit_document template on validation failure
    """
    if not (
        edit_form.is_submitted()
        and edit_form.validate(is_file_already_uploaded=not document.get("is_link"))
    ):

        return render_template(
            "./employee/update/edit_document.html",
            employee=employee,
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
                employee_repository.storage_path,
                title=edit_form.title.data,
            )
        else:
            uploaded_document = FileMapper.file_from_form(edit_form.data)

        if not uploaded_document:
            flash("No se pudo modificar el archivo, inténtelo nuevamente", "danger")
            return redirect(
                url_for("employee_bp.edit_documents", employee_id=employee["id"])
            )

    success = employee_repository.update_document(
        employee_id=employee["id"],
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

    return redirect(url_for("employee_bp.edit_documents", employee_id=employee["id"]))
