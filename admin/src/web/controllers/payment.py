from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dependency_injector.wiring import inject, Provide
from src.core.module.payment.forms import PaymentForm
from src.core.container import Container
from src.core.module.payment.services import PaymentServices
from src.core.module.payment.repositories import PaymentRepository

payment_bp = Blueprint(
    "payment_bp", __name__, template_folder="../templates/payment", url_prefix="/pago"
)


@payment_bp.route("/crear", methods=["GET", "POST"])
@inject
def create_payment(
    payment_service: PaymentServices = Provide[Container.payment_services],
):
    form = PaymentForm()
    if form.validate_on_submit():
        payment_data = {
            "amount": form.amount.data,
            "payment_date": form.date.data,
            "payment_type": form.payment_type.data,
            "description": form.description.data,
            "beneficiary_id": form.beneficiary_id.data if form.beneficiary_id.data else None,
        }
        payment_service.create_payment(payment_data)
        flash('Pago creado exitosamente', 'success')
        return redirect(url_for('payment_bp.create_payment'))
    else:
        flash('Error al crear el pago', 'danger')
    return render_template('payment/create_payment.html', form=form)
