from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dependency_injector.wiring import inject, Provide
from src.core.module.payment.forms import PaymentForm, PaymentSearchForm, PaymentEditForm
from src.core.container import Container
from src.web.helpers.auth import check_user_permissions
from src.core.module.payment.repositories import PaymentRepository
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
    form = PaymentSearchForm(request.form)
    search_query = {}
    order_by = []

    if form.validate_on_submit():
        if form.start_date.data:
            search_query["payment_date__gte"] = form.start_date.data
        if form.end_date.data:
            search_query["payment_date__lte"] = form.end_date.data
        if form.payment_type.data:
            search_query["payment_type"] = form.payment_type.data
        order_by = [(form.order_by.data, form.order.data)]
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    payments = payment_repository.get_page(page, per_page, 100, search_query, order_by)

    return render_template("payments.html", form=form, payments=payments, search_form=form)

@payment_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['pagos_create'])
@inject
def create_payment(
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    form = PaymentForm()
    if form.validate_on_submit() and form.amount.data:
        payment_data = {
            "amount": form.amount.data,
            "payment_date": form.date.data,
            "payment_type": form.payment_type.data,
            "description": form.description.data,
            "beneficiary_id": form.beneficiary_id.data if form.beneficiary_id.data else None,
        }
        payment_repository.add(PaymentMapper.to_entity(payment_data))
        flash('Pago creado exitosamente', 'success')
        return redirect(url_for('payment_bp.create_payment'))
    else:
        if(form.amount.data):
            flash('Error al crear el pago', 'danger')
    return render_template('payment/create_payment.html', form=form,  edit=False)


@payment_bp.route("/<int:payment_id>", methods=["GET"])
@check_user_permissions(permissions_required=['pagos_show'])
@inject
def show_payment(
    payment_id: int,
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    payment =PaymentMapper.from_entity(payment_repository.get_by_id(payment_id))
    return render_template("payment/payment.html", payment=payment)

@payment_bp.route("/editar/<int:payment_id>", methods=["GET", "POST"])
@inject
@check_user_permissions(permissions_required=['pagos_update'])
def edit_payment(
    payment_id: int,
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    payment =PaymentMapper.from_entity(payment_repository.get_by_id(payment_id))
    payment["amount"] = float(payment["amount"]) # Convierte el string de ammount a float 
    form = PaymentEditForm(data=payment)
    if form.validate_on_submit():
        payment_data = {
            "id": payment_id,
            "amount": form.amount.data,
            "payment_date": form.date.data,
            "payment_type": form.payment_type.data,
            "description": form.description.data,
            "beneficiary_id": form.beneficiary_id.data if form.beneficiary_id.data else None,
        }

        payment_repository.update(payment_id, payment_data)
        flash('Pago actualizado exitosamente', 'success')
        return redirect(url_for('payment_bp.show_payment', payment_id=payment_id))

    return render_template('payment/create_payment.html', form=form, payment=payment, edit=True)

@payment_bp.route("/eliminar", methods=["POST"])
@inject
@check_user_permissions(permissions_required=['pagos_destroy'])
def delete_payment(
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    payment_id = request.form["item_id"]
    payment_repository.delete(payment_id)
    flash('Pago eliminado exitosamente', 'success')
    return redirect(url_for('payment_bp.get_payments'))

@payment_bp.route("/archivados", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['pagos_index'])
@inject
def get_archived_payments(
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    form = PaymentSearchForm(request.form)
    search_query={}
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
    print (search_query)
    payments = payment_repository.get_page(page, per_page,100, search_query, order_by)
    return render_template("payments_archived.html", form=form, payments=payments, search_form=form)

@payment_bp.route("/archivar/<int:payment_id>", methods=["POST"])
@check_user_permissions(permissions_required=['pagos_destroy'])
@inject
def archive_payment(
    payment_id: int,
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    payment_repository.archive_payment(payment_id)
    flash('Pago archivado exitosamente', 'success')
    return redirect(url_for('payment_bp.get_payments'))

@payment_bp.route("/desarchivar/<int:payment_id>", methods=["POST"])
@check_user_permissions(permissions_required=['pagos_destroy'])
@inject
def unarchive_payment(
    payment_id: int,
    payment_repository: PaymentRepository = Provide[Container.payment_repository],
):
    payment_repository.unarchive_payment(payment_id)
    flash('Pago desarchivado exitosamente', 'success')
    return redirect(url_for('payment_bp.get_payments'))