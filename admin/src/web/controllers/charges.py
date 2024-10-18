from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.core.module.employee.forms import EmployeeMiniSearchForm, EmployeeSelectForm
from src.core.module.employee import EmployeeSearchForm
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


@charges_bp.route("/")
@check_user_permissions(permissions_required=["cobros_index"])
@inject
def get_charges(charges_repository: ACR = Provide[Container.charges_repository]):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    search = ChargeSearchForm(request.args)
    search_query = {}
    order_by = []

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

    paginated_charges = charges_repository.get_page(
        page=page, per_page=per_page, order_by=order_by, search_query=search_query
    )

    return render_template("charges.html", charges=paginated_charges, search_form=search)


@charges_bp.route("/<int:charge_id>")
@check_user_permissions(permissions_required=["cobros_show"])
@inject
def show_charge(charge_id: int,
                charges_repository: ACR = Provide[Container.charges_repository],
                employees_repository: AbstractEmployeeRepository = Provide[Container.employee_repository]):

    charge = charges_repository.get_by_id(charge_id)

    if not charge:
        flash(f"El cobro con ID = {charge_id} no existe", "danger")
        return get_charges()

    employee = employees_repository.get_employee(charge["employee_id"])
    if not employee:
        flash(f"El empleado asociado al cobro no existe", "danger")
        return

    jya = None
    # jya = jya_repository.get_jya(charge["jya_id"])
    return render_template('charge.html', charge=charge, employee=employee, jya=jya)


@charges_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["cobros_new"])
def create_charge():
    create_form = ChargeCreateForm()

    if request.method == "POST":
        return add_charge(create_form=create_form)

    return render_template("create_charge.html", form=create_form)


@inject
def add_charge(create_form: ChargeCreateForm, charges_repository: ACR = Provide[Container.charges_repository]):
    if not create_form.validate_on_submit():
        return render_template("create_charge.html", form=create_form)

    charge = charges_repository.add_charge(Mapper.to_entity(Mapper.from_form(create_form.data)))

    return redirect(url_for("charges_bp.show_charge", charge_id=charge["id"]))


@charges_bp.route("/editar/<int:charge_id>", methods=["GET", "POST", "PUT"])
@check_user_permissions(permissions_required=["cobros_update"])
@inject
def edit_charge(charge_id: int,
                charges_repository: ACR = Provide[Container.charges_repository],
                employee_services: AbstractEmployeeRepository = Provide[Container.employee_repository],
                ):
    # TODO: traerme el jya del cobro
    charge = charges_repository.get_by_id(charge_id)

    if not charge:
        flash(f"Su búsqueda no devolvió un cobro existente", "danger")
        return redirect(url_for("charges_bp.get_charges"))

    employee = employee_services.get_employee(charge["employee_id"])
    employee_info = f"{employee['name']} {employee['lastname']} (Email: {employee['email']})"
    edit_form = ChargeEditForm(data=charge, employee_id=employee["id"], employee_info=employee_info)

    if request.method in ["POST", "PUT"]:
        return update_charge(charge_id=charge_id, edit_form=edit_form)

    return render_template("edit_charge.html", form=edit_form, charge=charge)


@inject
def update_charge(charge_id: int, edit_form: ChargeEditForm,
                  charges_repository: ACR = Provide[Container.charges_repository]):
    if not edit_form.validate_on_submit():
        return render_template("edit_charge.html", form=edit_form)

    print(edit_form.data)
    charges_repository.update_charge(charge_id, Mapper.from_form(edit_form.data))

    return redirect(url_for("charges_bp.show_charge", charge_id=charge_id))


@charges_bp.route("/delete/", methods=["POST"])
@check_user_permissions(permissions_required=["cobros_destroy"])
@inject
def delete_charge(charges_repository: ACR = Provide[Container.charges_repository]):
    charge_id = request.form["item_id"]
    deleted = charges_repository.delete_charge(int(charge_id))
    if not deleted:
        flash("El cobro no ha podido ser eliminado, inténtelo nuevamente", "danger")

    flash("El cobro ha sido eliminado correctamente", "success")
    return redirect(url_for("charges_bp.get_charges"))


@charges_bp.route("/cambiar-empleado/<int:charge_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["cobros_update"])
@inject
def change_employee(
        charge_id: int,
        charges_repository: ACR = Provide[Container.charges_repository],
        employees: AbstractEmployeeRepository = Provide[Container.employee_repository],
):
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("per_page", type=int, default=10)
    search_query = {}

    search_employee = EmployeeMiniSearchForm(request.args)
    select_employee = EmployeeSelectForm()

    charge = charges_repository.get_by_id(charge_id)
    if not charge:
        flash(f"El cobro con ID = {charge_id} no existe", "danger")
        return redirect(url_for("charges_bp.get_charges"))

    if request.method == "GET" and search_employee.validate():
        search_fields = ["name", "email"]
        search_query = {"text": search_employee.search_text.data, "fields": search_fields}

    employees = employees.get_page(
        page=page, search_query=search_query, per_page=per_page
    )

    if request.method == "POST":
        return add_charge_employee(charge, search_employee, select_employee, employees)

    return render_template(
        "./charges/update_employee.html",
        charge=charge,
        employees=employees,
        search_form=search_employee,
        select_form=select_employee,
    )


@inject
def add_charge_employee(
        charge,
        search_form,
        select_form,
        paginated_employees,
        charges_repository: ACR = Provide[Container.charges_repository],
):
    if not (select_form.submit_employee.data and select_form.validate()):
        return render_template(
            "./charges/update_employee.html",
            charge=charge,
            employees=paginated_employees,
            search_form=search_form,
            select_form=select_form,
        )

    charge_id = charge.get("id")
    employee_id = select_form.selected_employee.data

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


@charges_bp.route("/cambiar-jya/<int:charge_id>", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["cobros_update"])
@inject
def change_jya(charge_id: int,
               ):
    pass
