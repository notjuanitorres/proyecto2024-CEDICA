from flask import Blueprint, jsonify, render_template, request, url_for, redirect, flash
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.employee.forms import EmployeeSearchForm
from src.core.module.employee import (
    EmployeeMapper as Mapper,
    AbstractEmployeeServices,
    EmployeeCreateForm,
    EmployeeEditForm,
    enums as employment_information,
)


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
        if search.filter_profession.data:
            search_query["filters"] = {"profession": search.filter_profession.data}

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
):
    if not create_form.validate_on_submit():
        return render_template("./employee/create_employee.html", form=create_form)

    created_employee = employees.create_employee(Mapper.from_form(create_form.data))

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
        data=Mapper.to_form(employee),
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

    if not employees.update_employee(employee_id, Mapper.from_form(update_form.data)):
        flash("No se ha podido actualizar al miembro del equipo", "success")
        return render_template("./employee/update_employee.html")

    flash("El miembro del equipo ha sido actualizado exitosamente ")
    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))

@employee_bp.route("/api", methods=["GET"])
@check_user_permissions(permissions_required=["equipo_index"])
@inject
def api_get_employees(
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
):
    search_query = request.args.get("search", type=str, default="")
    search_query = search_query.strip().lower()

    if not search_query:
        return jsonify([])

    search_results = employees.search_by_email(search_query)

    return jsonify([
        {
            "id": employee.id,
            "name": employee.fullname,
            "email": employee.email,
        }
        for employee in search_results
    ])