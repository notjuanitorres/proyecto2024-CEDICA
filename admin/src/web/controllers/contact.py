from flask import Blueprint, render_template, request, redirect, url_for, flash
from dependency_injector.wiring import inject, Provide
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
from src.core.module.contact import AbstractContactRepository, ContactSearchForm

contact_bp = Blueprint("contact_bp", __name__, url_prefix="/contact")


@contact_bp.route("/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['mensaje_index'])
@inject
def get_messages(
    contact_repository: AbstractContactRepository = Provide[Container.contact_repository],
):
    """
    Route to get a paginated list of messages.

    Args:
        contact_repository (publicationRepository): The messages repository.

    Returns:
        Response: The rendered template for the list of messages (str).
    """
    form = ContactSearchForm(request.args)
    search_query: dict = {}
    order_by = []
    if form.submit_search.data and form.validate():
        search_query = {"text": form.search_text.data, "field": form.search_by.data}

        if form.start_date.data:
            search_query["filters"]["start_date"] = form.start_date.data
        if form.end_date.data:
            search_query["filters"]["end_date"] = form.end_date.data
        if form.filter_status.data:
            search_query["filters"]["status"] = form.filter_status.data
        if form.order_by.data and form.order.data:
            order_by = [(form.order_by.data, form.order.data)]

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    messages = contact_repository.get_page(page, per_page, search_query, order_by)

    return render_template("./contact/messages.html",
                           search_form=form, messages=messages)
