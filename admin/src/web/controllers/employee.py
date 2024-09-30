from flask import Blueprint, render_template, request, url_for, redirect
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.employee import AbstractEmployeeServices


employee_bp = Blueprint(
    "employee_bp",
    __name__,
    template_folder="templates/employee/",
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


@employee_bp.route("/crear")
@inject
def create_employee(
    employees: AbstractEmployeeServices = Provide[Container.employee_services],
):
    return redirect(url_for("employee_bp.get_employees"))


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


@employee_bp.route("/editar/<int:employee_id>")
@inject
def edit_employee(
    employee_id: int,
    employees: AbstractEmployeeServices = Provide[Container.employee_services]
):
    return redirect(url_for("employee_bp.get_employees"))
