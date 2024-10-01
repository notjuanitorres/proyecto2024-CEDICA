from flask import Blueprint, render_template, request, url_for, redirect
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.employee import (
    EmployeeDTO,
    AbstractEmployeeServices,
    EmployeeCreateForm,
    EmployeeEditForm,
)


employee_bp = Blueprint(
    "employee_bp",
    __name__,
    template_folder="./templates/employee/",
    url_prefix="/equipo/",
)


@employee_bp.route("/")
@check_user_permissions(permissions_required=["equipo_index"])
@inject
def get_employees(
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
):
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    order_by = [(sort_by, order)]

    paginated_employees = employees.get_page(
        page=page, per_page=per_page, order_by=order_by
    )

    return render_template("./employee/employees.html", employees=paginated_employees)


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
    
    created_employee = employees.create_employee(
        EmployeeDTO.from_form(create_form.data)
    )
    return redirect(
        url_for("employee_bp.show_employee", employee_id=created_employee.id)
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

    update_form = EmployeeEditForm(data=employee.to_form())

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
    if not update_form.validate_on_submit():
        return render_template("./employee/update_employee.html", form=update_form)

    return redirect(url_for("employee_bp.show_employee", employee_id=employee_id))
