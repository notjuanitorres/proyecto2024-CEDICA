from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from src.core.module.jockey_amazon.forms import JockeyAmazonMiniSearchForm, JockeyAmazonSelectForm
from src.core.module.jockey_amazon.repositories import AbstractJockeyAmazonRepository
from src.core.module.employee.forms import EmployeeMiniSearchForm, EmployeeSelectForm
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from dependency_injector.wiring import inject, Provide
from src.core.module.charges.forms import ChargeSearchForm, ChargeCreateForm, ChargeEditForm
from src.core.module.charges import (
    AbstractChargeRepository as ACR,
    ChargeMapper as Mapper
)
from src.core.module.employee import AbstractEmployeeRepository

charges_bp = Blueprint(
    "charges_bp", __name__, template_folder="../templates/charges", url_prefix="/cobros"
)


@inject
def search_charges(search: ChargeSearchForm,
                   need_archived: bool = False,
                   charges_repository: ACR = Provide[Container.charges_repository]):
    """
    Search for charges based on the provided search form and filters.

    Args:
        search (ChargeSearchForm): The form containing search criteria.
        need_archived (bool): Whether to include archived charges in the search.
        charges_repository (ACR): The repository for charge data.

    Returns:
        A paginated list of charges matching the search criteria.
    """
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    order_by = [("date_of_charge", "desc")]
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
        if search.filter_payment_method.data:
            search_query["filters"] = {"payment_method": search.filter_payment_method.data}

        if search.start_date.data and search.finish_date.data:
            if "filters" not in search_query:
                search_query["filters"] = {}
            search_query["filters"]["start_date"] = search.start_date.data
            search_query["filters"]["finish_date"] = search.finish_date.data

    return charges_repository.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )


@inject
def search_jyas(search: JockeyAmazonMiniSearchForm,
                select_form: JockeyAmazonSelectForm,
                jya_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository]):
    """
    Search for jockeys or amazons based on the provided search form.

    Args:
        search (JockeyAmazonMiniSearchForm): The form containing search criteria.
        select_form (JockeyAmazonSelectForm): The form for selecting a jockey or amazon.
        jya_repository (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A paginated list of jockeys or amazons matching the search criteria.
    """
    page = request.args.get("page", type=int)

    jyas = []
    if request.method == "GET":
        if search.validate():
            jyas = jya_repository.get_active_jockeys(page=page, search=search.search_text.data)
        else:
            jyas = jya_repository.get_active_jockeys(page=page)

    if request.method == "POST":
        if not (select_form.submit_jya.data and select_form.validate()):
            jyas = jya_repository.get_active_jockeys(page=page)

    return jyas


@charges_bp.route("/")
@check_user_permissions(permissions_required=["cobros_index"])
def get_charges():
    """
    Display a list of charges.

    Returns:
        A rendered template displaying the list of charges and the search form.
    """
    search = ChargeSearchForm(request.args)

    paginated_charges = search_charges(search=search, need_archived=False)

    return render_template("./charges/charges.html", charges=paginated_charges, search_form=search)


@charges_bp.route("/archivados", methods=["GET"])
@check_user_permissions(permissions_required=["cobros_index"])
def get_archived_charges():
    """
    Display a list of archived charges.

    Returns:
        A rendered template displaying the list of archived charges and the search form.
    """
    search_form = ChargeSearchForm(request.args)
    paginated_charges = search_charges(search=search_form, need_archived=True)
    return render_template(
        "./charges/charges_archived.html",
        charges=paginated_charges,
        search_form=search_form,
    )


@charges_bp.route("/<int:charge_id>")
@check_user_permissions(permissions_required=["cobros_show"])
@inject
def show_charge(charge_id: int,
                charges_repository: ACR = Provide[Container.charges_repository],
                employees_repository: AbstractEmployeeRepository = Provide[Container.employee_repository],
                jya_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],):
    """
    Display the details of a specific charge.

    Args:
        charge_id (int): The ID of the charge to display.
        charges_repository (ACR): The repository for charge data.
        employees_repository (AbstractEmployeeRepository): The repository for employee data.
        jya_repository (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A rendered template displaying the charge's details and associated employee and jockey/amazon information.
    """
    charge = charges_repository.get_by_id(charge_id)

    if not charge:
        flash(f"El cobro con ID = {charge_id} no existe", "danger")
        return get_charges()

    employee = employees_repository.get_employee(charge["employee_id"])
    if not employee:
        flash(f"El empleado asociado al cobro no existe", "danger")
        return get_charges()

    jya = jya_repository.get_by_id(charge["jya_id"])
    if not jya:
        flash(f"El Jockey/Amazon asociado al cobro no existe", "danger")
        return get_charges()
    return render_template('./charges/charge.html', charge=charge, employee=employee, jya=jya)


@charges_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["cobros_new"])
def create_charge():
    """
    Display the form to create a new charge and handle form submission.

    Returns:
        A rendered template displaying the charge creation form,
         or a redirect to the employee linking page if successful.
    """
    create_form = ChargeCreateForm()

    if request.method == "POST":
        return add_charge(create_form=create_form)

    return render_template("./charges/create_charge.html", form=create_form)


@inject
def add_charge(create_form: ChargeCreateForm):
    """
    Add a new charge to the system.

    Args:
        create_form (ChargeCreateForm): The form containing the new charge's information.

    Returns:
        A rendered template displaying the charge creation form if validation fails,
         or a redirect to the employee linking page if successful.
    """
    if not create_form.validate_on_submit():
        return render_template("./charges/create_charge.html", form=create_form)

    session["charge"] = Mapper.to_session(Mapper.from_form(create_form.data))

    flash("Datos del cobro enviados correctamente!", "success")
    return redirect(url_for("charges_bp.link_employee"))


@charges_bp.route("/editar/<int:charge_id>", methods=["GET", "POST", "PUT"])
@check_user_permissions(permissions_required=["cobros_update"])
@inject
def edit_charge(charge_id: int,
                charges_repository: ACR = Provide[Container.charges_repository],
                employee_services: AbstractEmployeeRepository = Provide[Container.employee_repository],
                ):
    """
    Display the form to edit an existing charge and handle form submission.

    Args:
        charge_id (int): The ID of the charge to edit.
        charges_repository (ACR): The repository for charge data.
        employee_services (AbstractEmployeeRepository): The repository for employee data.

    Returns:
        A rendered template displaying the charge edit form,
         or a redirect to the charge list page if the charge does not exist.
    """
    charge = charges_repository.get_by_id(charge_id)

    if not charge:
        flash(f"Su búsqueda no devolvió un cobro existente", "danger")
        return redirect(url_for("charges_bp.get_charges"))

    employee = employee_services.get_employee(charge["employee_id"])
    employee_info = f"{employee['name']} {employee['lastname']} (Email: {employee['email']})"
    edit_form = ChargeEditForm(data=charge, employee_id=employee["id"], employee_info=employee_info)

    if request.method in ["POST", "PUT"]:
        return update_charge(charge_id=charge_id, edit_form=edit_form)

    return render_template("./charges/edit_charge.html", form=edit_form, charge=charge)


@inject
def update_charge(charge_id: int, edit_form: ChargeEditForm,
                  charges_repository: ACR = Provide[Container.charges_repository]):
    """
    Update an existing charge's information.

    Args:
        charge_id (int): The ID of the charge to update.
        edit_form (ChargeEditForm): The form containing the updated charge information.
        charges_repository (ACR): The repository for charge data.

    Returns:
        A rendered template displaying the charge edit form if validation fails,
         or a redirect to the charge detail page if successful.
    """
    if not edit_form.validate_on_submit():
        return render_template("./charges/edit_charge.html", form=edit_form)

    success = charges_repository.update_charge(charge_id, Mapper.from_form(edit_form.data))

    if success:
        flash("El cobro se modificó correctamente!", "success")
    else:
        flash("El cobro no pudo ser modificado, inténtelo nuevamente", "danger")
    return redirect(url_for("charges_bp.show_charge", charge_id=charge_id))


@charges_bp.route("/delete/", methods=["POST"])
@check_user_permissions(permissions_required=["cobros_destroy"])
@inject
def delete_charge(charges_repository: ACR = Provide[Container.charges_repository]):
    """
    Delete a charge.

    Args:
        charges_repository (ACR): The repository for charge data.

    Returns:
        A redirect to the charge list page.
    """
    charge_id = request.form["item_id"]
    try:
        charge_id = int(charge_id)
    except ValueError:
        flash("El cobro solicitado no existe", "danger")
        return redirect(url_for("charges_bp.get_charges"))

    deleted = charges_repository.delete_charge(charge_id)
    if not deleted:
        flash("El cobro no ha podido ser eliminado, inténtelo nuevamente", "danger")
    else:
        flash("El cobro ha sido eliminado correctamente", "success")
    return redirect(url_for("charges_bp.get_charges"))


@charges_bp.route("/archivar/", methods=["POST"])
@check_user_permissions(permissions_required=["cobros_destroy"])
@inject
def archive_charge(
    charges_repository: ACR = Provide[Container.charges_repository],
):
    """
    Archive a charge.

    Args:
        charges_repository (ACR): The repository for charge data.

    Returns:
        A redirect to the charge detail page.
    """
    charge_id = request.form["item_id"]
    try:
        charge_id = int(charge_id)
    except ValueError:
        flash("El cobro solicitado no existe", "danger")
        return redirect(url_for("charges_bp.get_charges"))

    archived = charges_repository.archive_charge(charge_id)

    if not archived:
        flash("El cobro no existe o ya ha sido archivado", "warning")
    else:
        flash("El cobro ha sido archivado correctamente", "success")
    return redirect(url_for("charges_bp.show_charge", charge_id=charge_id))


@charges_bp.route("/recuperar/", methods=["POST"])
@check_user_permissions(permissions_required=["cobros_destroy"])
@inject
def recover_charge(
    charges: ACR = Provide[Container.charges_repository],
):
    """
    Recover an archived charge.

    Args:
        charges (ACR): The repository for charge data.

    Returns:
        A redirect to the charge detail page.
    """
    charge_id = request.form["charge_id"]
    try:
        charge_id = int(charge_id)
    except ValueError:
        flash("El cobro solicitado no existe", "danger")
        return redirect(url_for("charges_bp.get_charges"))
    recovered = charges.recover_charge(charge_id)

    if not recovered:
        flash("El cobro no existe o no puede ser recuperado", "warning")
    else:
        flash("El cobro ha sido recuperado correctamente", "success")
    return redirect(url_for("charges_bp.show_charge", charge_id=charge_id))


@charges_bp.route("/asignar-empleado/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["cobros_update"])
@inject
def link_employee(
        employee_repository: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    """
    Link an employee to a charge.

    Args:
        employee_repository (AbstractEmployeeRepository): The repository for employee data.

    Returns:
        A rendered template displaying the employee linking form,
         or a redirect to the charge list page if the session does not contain charge data.
    """
    if not session.get("charge"):
        flash(f"Esta pagina solo puede ser accedida al crear un cobro", "danger")
        return redirect(url_for("charges_bp.get_charges"))

    charge = Mapper.from_session(session.get("charge"))
    page = request.args.get("page", type=int, default=1)

    search_employee = EmployeeMiniSearchForm(request.args)
    select_employee = EmployeeSelectForm()

    employees = []
    if request.method == "GET":
        if search_employee.validate():
            employees = employee_repository.get_active_employees(
                [], page=page, search=search_employee.search_text.data
            )
        else:
            employees = employee_repository.get_active_employees([], page=page)

    if request.method == "POST":
        if not (select_employee.submit_employee.data and select_employee.validate()):
            flash("No se ha seleccionado un empleado", "danger")
            employees = employee_repository.get_active_employees([], page=page)
        return link_charge_employee(charge, search_employee, select_employee, employees)

    return render_template(
        "./charges/create_employee.html",
        charge=charge,
        employees=employees,
        search_form=search_employee,
        select_form=select_employee,
    )


@inject
def link_charge_employee(
        charge,
        search_form,
        select_form,
        paginated_employees,
):
    """
    Link an employee to a charge.

    Args:
        charge: The charge data.
        search_form: The form containing search criteria for employees.
        select_form: The form for selecting an employee.
        paginated_employees: The paginated list of employees.

    Returns:
        A rendered template displaying the employee linking form if validation fails,
         or a redirect to the jockey/amazon linking page if successful.
    """
    if not (select_form.submit_employee.data and select_form.validate()):
        return render_template(
            "./charges/create_employee.html",
            charge=charge,
            employees=paginated_employees,
            search_form=search_form,
            select_form=select_form,
        )

    employee_id = select_form.selected_item.data

    session["charge"]["employee_id"] = employee_id

    flash("El empleado asociado al cobro se envio correctamente!", "success")
    return redirect(url_for("charges_bp.link_jya"))


@charges_bp.route("/asignar-jya/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["cobros_update"])
@inject
def link_jya(
):
    """
    Link a jockey or amazon to a charge.

    Returns:
        A rendered template displaying the jockey/amazon linking form,
         or a redirect to the charge list page if the session does not contain charge data.
    """
    if not session.get("charge"):
        flash(f"Esta pagina solo puede ser accedida al crear un cobro", "danger")
        return redirect(url_for("charges_bp.get_charges"))

    charge = Mapper.from_session(session.get("charge"))

    search_jya = JockeyAmazonMiniSearchForm(request.args)
    select_jya = JockeyAmazonSelectForm()

    jyas = search_jyas(search_jya, select_jya)

    if request.method == "POST":
        return link_charge_jya(charge, search_jya, select_jya, jyas)

    return render_template(
        "./charges/create_jya.html",
        charge=charge,
        jyas=jyas,
        search_form=search_jya,
        select_form=select_jya,
    )


@inject
def link_charge_jya(
        charge,
        search_form,
        select_form,
        paginated_jyas,
        charges_repository: ACR = Provide[Container.charges_repository],
):
    """
    Link a jockey or amazon to a charge.

    Args:
        charge: The charge data.
        search_form: The form containing search criteria for jockeys or amazons.
        select_form: The form for selecting a jockey or amazon.
        paginated_jyas: The paginated list of jockeys or amazons.
        charges_repository (ACR): The repository for charge data.

    Returns:
        A rendered template displaying the jockey/amazon linking form if validation fails,
         or a redirect to the charge detail page if successful.
    """
    if not (select_form.submit_jya.data and select_form.validate()):
        flash("No se ha seleccionado un Jinete o amazona", "danger")
        return render_template(
            "./charges/create_jya.html",
            charge=charge,
            jyas=paginated_jyas,
            search_form=search_form,
            select_form=select_form,
        )

    jya_id = select_form.selected_item.data

    session["charge"]["jya_id"] = jya_id

    charge = Mapper.from_session(session.get("charge"))
    charge = charges_repository.add_charge(Mapper.to_entity(charge))
    session.pop("charge")

    flash("El cobro se creo correctamente!", "success")
    return redirect(url_for("charges_bp.show_charge", charge_id=charge["id"]))


@inject
def add_charge_employee(
        charge,
        search_form,
        select_form,
        paginated_employees,
        charges_repository: ACR = Provide[Container.charges_repository],
):
    """
    Add an employee to a charge.

    Args:
        charge: The charge object to update.
        search_form: The form used to search for employees.
        select_form: The form used to select an employee.
        paginated_employees: The paginated list of employees.
        charges_repository (ACR): The repository for charge data.

    Returns:
        A rendered template displaying the update employee form if validation fails,
        or a redirect to the charge detail page if successful.
    """
    if not (select_form.submit_employee.data and select_form.validate()):
        return render_template(
            "./charges/update_employee.html",
            charge=charge,
            employees=paginated_employees,
            search_form=search_form,
            select_form=select_form,
        )

    charge_id = charge.get("id")
    employee_id = select_form.selected_item.data

    if charges_repository.update_charge(charge_id, {"employee_id": employee_id}):
        flash(
            f"Se ha cambiado correctamente el empleado",
            "success",
        )
    else:
        flash(
            f"No se ha podido cambiar el empleado",
            "danger",
        )
    return redirect(url_for("charges_bp.show_charge", charge_id=charge_id))


@inject
def add_charge_jya(
    charge,
    search_form,
    select_form,
    paginated_jyas,
    charges_repository: ACR = Provide[Container.charges_repository],
):
    """
    Add a jockey or amazon to a charge.

    Args:
        charge: The charge object to update.
        search_form: The form used to search for jockeys or amazons.
        select_form: The form used to select a jockey or amazon.
        paginated_jyas: The paginated list of jockeys or amazons.
        charges_repository (ACR): The repository for charge data.

    Returns:
        A rendered template displaying the update jockey/amazon form if validation fails,
        or a redirect to the charge detail page if successful.
    """
    if not (select_form.submit_jya.data and select_form.validate()):
        return render_template(
            "./charges/update_jya.html",
            charge=charge,
            jyas=paginated_jyas,
            search_form=search_form,
            select_form=select_form,
        )

    charge_id = charge.get("id")
    jya_id = select_form.selected_item.data

    if charges_repository.update_charge(charge_id, {"jya_id": jya_id}):
        flash(
            "Se ha cambiado correctamente el Jockey/Amazon",
            "success",
        )
    else:
        flash(
            "No se ha podido cambiar el Jockey/Amazon",
            "danger",
        )
    return redirect(url_for("charges_bp.show_charge", charge_id=charge_id))


@charges_bp.route("/elegir-deudor/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["cobros_update"])
@inject
def choose_debtor(
):
    """
    Choose a debtor for a charge.

    Returns:
        A rendered template displaying the choose debtor form if validation fails,
        or a redirect to the charge detail page if successful.
    """
    search_jya = JockeyAmazonMiniSearchForm(request.args)
    select_jya = JockeyAmazonSelectForm()
    select_jya.submit_jya.label.text = "Cambiar estado"

    jyas = search_jyas(search_jya, select_jya)

    if request.method == "POST":
        return toggle_debtor_status(search_jya, select_jya, jyas)

    return render_template(
        "./charges/choose_debtor.html",
        jyas=jyas,
        search_form=search_jya,
        select_form=select_jya,
    )


@charges_bp.route("/cambiar-estado-deudor/", methods=["POST"])
@check_user_permissions(permissions_required=["cobros_update"])
@inject
def toggle_debtor_status(
        search_form: JockeyAmazonMiniSearchForm,
        select_form: JockeyAmazonSelectForm,
        jyas,
        jya_repository: AbstractJockeyAmazonRepository = Provide[Container.jockey_amazon_repository],
):
    """
    Toggle the debtor status of a jockey or amazon.

    Args:
        search_form (JockeyAmazonMiniSearchForm): The form used to search for jockeys or amazons.
        select_form (JockeyAmazonSelectForm): The form used to select a jockey or amazon.
        jyas: The list of jockeys or amazons.
        jya_repository (AbstractJockeyAmazonRepository): The repository for jockey and amazon data.

    Returns:
        A rendered template displaying the choose debtor form if validation fails,
        or a redirect to the charge detail page if successful.
    """
    if not (select_form.submit_jya.data and select_form.validate()):
        flash("No se ha seleccionado un Jinete o amazona", "danger")
        return render_template(
            "./charges/choose_debtor.html",
            jyas=jyas,
            search_form=search_form,
            select_form=select_form,
        )

    jya_id = select_form.selected_item.data
    updated = jya_repository.toggle_debtor_status(jya_id)

    if not updated:
        flash("El estado de deudor no pudo ser cambiado", "danger")
    else:
        flash("El estado de deudor ha sido cambiado correctamente", "success")
    return redirect(url_for("charges_bp.get_charges"))
