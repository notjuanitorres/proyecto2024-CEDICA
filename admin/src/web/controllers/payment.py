from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dependency_injector.wiring import inject, Provide
from src.core.module.employee.forms import EmployeeSearchForm, EmployeeSelectForm, EmployeeMiniSearchForm
from src.core.module.employee.repositories import AbstractEmployeeRepository as EmployeeRepository
from src.core.module.payment.forms import PaymentForm, PaymentSearchForm, PaymentEditForm
from src.core.container import Container
from src.web.helpers.auth import check_user_permissions
from src.core.module.payment.repositories import AbstractPaymentRepository as PaymentRepository
from src.core.module.payment.mappers import PaymentMapper


payment_bp = Blueprint(
    "payment_bp", __name__, template_folder="../templates/payment", url_prefix="/pago"
)


@payment_bp.route("/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['pagos_index'])
@inject
def get_payments(
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    """
    Route to get a paginated list of payments.

    Args:
        payment_repository (PaymentRepository): The payment repository.

    Returns:
        Response: The rendered template for the list of payments (str).
    """
    form = PaymentSearchForm(request.args)
    search_query = {}
    order_by = []

    if form.validate():
        if form.start_date.data:
            search_query["payment_date__gte"] = form.start_date.data
        if form.end_date.data:
            search_query["payment_date__lte"] = form.end_date.data
        if form.payment_type.data:
            search_query["payment_type"] = form.payment_type.data
        if form.order_by.data and form.order.data:
            order_by = [(form.order_by.data, form.order.data)]
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search_query["is_archived"] = False

    payments = payment_repository.get_page(page, per_page, search_query, order_by)

    return render_template("./payment/payments.html", form=form, payments=payments)


@payment_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['pagos_new'])
@inject
def create_payment(
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    """
    Route to create a new payment.

    Args:
        payment_repository (PaymentRepository): The payment repository.

    Returns:
        Response: The rendered template for creating a payment (str).
    """
    form = PaymentForm()
    if form.validate_on_submit() and form.amount.data:
        payment_data = {
            "amount": form.amount.data,
            "payment_date": form.date.data,
            "payment_type": form.payment_type.data,
            "description": form.description.data,
            "beneficiary_id": None,
        }
        if form.payment_type.data == 'HONORARIOS':
            session["payment"] = payment_data
            return redirect(url_for('payment_bp.select_employee'))
        else:
            payment_repository.add(PaymentMapper.to_entity(payment_data))
        flash('Pago creado exitosamente', 'success')
        return redirect(url_for('payment_bp.get_payments'))
    else:
        if form.amount.data:
            flash('Error al crear el pago', 'danger')
    return render_template('payment/create_payment.html', form=form,  edit=False)


@payment_bp.route("/<int:payment_id>", methods=["GET"])
@check_user_permissions(permissions_required=['pagos_show'])
@inject
def show_payment(
    payment_id: int,
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
        employee_repository: EmployeeRepository = Provide[Container.employee_repository],
):
    """
    Route to show details of a specific payment.

    Args:
        payment_id (int): The ID of the payment.
        payment_repository (PaymentRepository): The payment repository.
        employee_repository (EmployeeRepository): The employee repository.

    Returns:
        Response: The rendered template for the payment details (str).
    """
    payment = PaymentMapper.from_entity(payment_repository.get_by_id(payment_id))
    beneficiary = employee_repository.get_employee(payment["beneficiary_id"]) if payment["beneficiary_id"] else {}
    return render_template("payment/payment.html", payment=payment, beneficiary=beneficiary)


@payment_bp.route("/editar/<int:payment_id>", methods=["GET", "POST"])
@inject
@check_user_permissions(permissions_required=['pagos_update'])
def edit_payment(
    payment_id: int,
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
    employee_repository: EmployeeRepository = Provide[Container.employee_repository],
):
    """
    Route to edit an existing payment.

    Args:
        payment_id (int): The ID of the payment.
        payment_repository (PaymentRepository): The payment repository.
        employee_repository (EmployeeRepository): The employee repository.

    Returns:
        Response: The rendered template for editing a payment (str).
    """
    payment = PaymentMapper.from_entity(payment_repository.get_by_id(payment_id))
    payment["amount"] = float(payment["amount"])  # Convierte el string de ammount a float
    beneficiary = employee_repository.get_employee(payment["beneficiary_id"]) if payment["beneficiary_id"] else {}
    form = PaymentEditForm(data=payment)
    if form.validate_on_submit():
        payment_data = {
            "amount": form.amount.data,
            "payment_date": form.date.data,
            "payment_type": form.payment_type.data,
            "description": form.description.data,
            "beneficiary_id": form.beneficiary_id.data if form.beneficiary_id.data else None,
        }

        payment_repository.update(payment_id, payment_data)
        flash('Pago actualizado exitosamente', 'success')
        return redirect(url_for('payment_bp.show_payment', payment_id=payment_id))

    return render_template('payment/create_payment.html',
                           form=form, payment=payment, edit=True, beneficiary=beneficiary)


@payment_bp.route("/eliminar", methods=["POST"])
@inject
@check_user_permissions(permissions_required=['pagos_destroy'])
def delete_payment(
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    """
    Route to delete a payment.

    Args:
        payment_repository (PaymentRepository): The payment repository.

    Returns:
        Response: Redirect to the list of archived payments.
    """
    payment_id = request.form["item_id"]

    try:
        payment_id = int(payment_id)
    except ValueError:
        flash('El pago solicitado no existe', 'danger')
        return redirect(url_for('payment_bp.get_payments'))

    success = payment_repository.delete(payment_id)
    if not success:
        flash('El pago solicitado no existe', 'danger')
    else:
        flash('Pago eliminado exitosamente', 'success')
    return redirect(url_for('payment_bp.get_archived_payments'))


@payment_bp.route("/archivados", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['pagos_index'])
@inject
def get_archived_payments(
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    """
    Route to get a paginated list of archived payments.

    Args:
        payment_repository (PaymentRepository): The payment repository.

    Returns:
        Response: The rendered template for the list of archived payments (str).
    """
    form = PaymentSearchForm(request.args)
    
    search_query = {}
    order_by = []

    if form.validate():
        if form.start_date.data:
            search_query["payment_date__gte"] = form.start_date.data
        if form.end_date.data:
            search_query["payment_date__lte"] = form.end_date.data
        if form.payment_type.data:
            search_query["payment_type"] = form.payment_type.data
        order_by = [(form.order_by.data, form.order.data)]
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    search_query["is_archived"] = True

    payments = payment_repository.get_page(page, per_page, search_query, order_by)
    return render_template("./payment/payments_archived.html", form=form, payments=payments)


@payment_bp.route("/archivar", methods=["POST"])
@check_user_permissions(permissions_required=['pagos_destroy'])
@inject
def archive_payment(
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    """
    Route to archive a payment.

    Args:
        payment_repository (PaymentRepository): The payment repository.

    Returns:
        Response: Redirect to the list of payments.
    """
    payment_id = request.form["item_id"]
    success = payment_repository.archive_payment(payment_id)
    if success:
        flash('Pago archivado exitosamente', 'success')
    else:
        flash('El pago ya esta archivado o no existe', 'danger')
    return redirect(url_for('payment_bp.get_payments'))


@payment_bp.route("/desarchivar/<int:payment_id>", methods=["POST"])
@check_user_permissions(permissions_required=['pagos_destroy'])
@inject
def unarchive_payment(
    payment_id: int,
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    """
    Route to unarchive a payment.

    Args:
        payment_id (int): The ID of the payment.
        payment_repository (PaymentRepository): The payment repository.

    Returns:
        Response: Redirect to the list of payments.
    """
    success = payment_repository.unarchive_payment(payment_id)
    if success:
        flash('Pago desarchivado exitosamente', 'success')
    else:
        flash('El pago ya esta desarchivado o no existe', 'danger')
    return redirect(url_for('payment_bp.get_payments'))


@payment_bp.route("/select_employee", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['pagos_new'])
@inject
def select_employee(
    employee_repository: EmployeeRepository = Provide[Container.employee_repository],
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    """
    Route to select an employee as the beneficiary of a payment.

    Args:
        employee_repository (EmployeeRepository): The employee repository.
        payment_repository (PaymentRepository): The payment repository.

    Returns:
        Response: The rendered template for selecting an employee (str).
    """
    page = request.args.get("page", type=int, default=1)

    search_employee = EmployeeMiniSearchForm(request.args)
    select_form = EmployeeSelectForm()

    employees = []
    if request.method == "GET":
        if search_employee.validate():
            employees = employee_repository.get_active_employees(
                [], page=page, search=search_employee.search_text.data
            )
        else:
            employees = employee_repository.get_active_employees([], page=page)

    if request.method == "POST" and select_form.validate_on_submit():
        selected_employee_id = select_form.selected_item.data
        payment_data = session["payment"]
        session.pop("payment", None)
        payment_data["beneficiary_id"] = selected_employee_id
        pago_entity = PaymentMapper.to_entity(payment_data)
        pago_entity = payment_repository.add(pago_entity)
        flash('Pago creado exitosamente', 'success')
        return redirect(url_for('payment_bp.show_payment', payment_id=pago_entity.id))

    return render_template("payment/select_employee.html",
                           search_form=search_employee, select_form=select_form, employees=employees)
