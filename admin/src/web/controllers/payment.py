from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dependency_injector.wiring import inject, Provide
from src.core.module.payment.forms import PaymentForm
from src.core.container import Container
from src.web.helpers.auth import check_user_permissions

payment_bp = Blueprint(
    "payment_bp", __name__, template_folder="../templates/payment", url_prefix="/pago"
)


@payment_bp.route("/crear", methods=["GET", "POST"])
def create_payment():
    create_form = PaymentForm()
    if not check_user_permissions(permissions_required=["ecuestre_new"]):
       return redirect(url_for("index_bp.home"))

    if request.method == "POST":
        return ()

    return render_template("create_payment.html", form=create_form)
