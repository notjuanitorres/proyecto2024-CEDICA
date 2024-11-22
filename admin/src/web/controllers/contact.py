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


@contact_bp.route("/<int:message_id>")
@check_user_permissions(permissions_required=["mensaje_show"])
@inject
def show_message(message_id: int,
               contact_repository: AbstractContactRepository = Provide[Container.contact_repository]):
    """
    Route to show details of a specific message.

    Args:
        message_id (int): The ID of the message.
        contact_repository (AbstractContactRepository): The contact repository.

    Returns:
        Response: The rendered template for the message details if the message exists,
         otherwise redirect to the list of messages.
    """
    message = contact_repository.get_by_id(message_id)
    if not message:
        flash(f"El mensaje con ID = {message_id} no existe", "danger")
        return get_messages()

    return render_template('./contact/message.html', message=message)

