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
    search_form = ContactSearchForm(request.args)

    paginated_messages = search_messages(search=search_form, need_archive=False)

    return render_template(
        "./contact/list/messages.html",
        messages=paginated_messages,
        search_form=search_form,
    )


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

@contact_bp.route("/archivados", methods=["GET"])
@check_user_permissions(permissions_required=["mensaje_index"])
def get_deleted_messages():
    """
    Retrieve and display a paginated list of archived messages.

    Returns:
        rendered template: The messages_archived.html template with:
            - paginated archived messages list
            - message information
            - search form
    """
    search_form = ContactSearchForm(request.args)
    paginated_messages = search_messages(search=search_form, need_archive=True)
    return render_template(
        "./contact/list/deleted_messages.html",
        messages=paginated_messages,
        search_form=search_form,
    )

@inject
def search_messages(
        search: ContactSearchForm,
        need_archive: bool,
        messages: AbstractContactRepository = Provide[Container.contact_repository],
):
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("per_page", type=int, default=10)
    order_by = []
    search_query = {
        "filters": {
            "is_deleted": need_archive,
        }
    }
    if search.submit_search.data:
        order_by = [(search.order_by.data, search.order.data)]
        search_query["text"] = search.search_text.data
        search_query["field"] = search.search_by.data
        if search.filter_status.data:
            search_query["filters"]["status"] = search.filter_status.data

    paginated_messages = messages.get_page(
        page=page,
        per_page=per_page,
        order_by=order_by,
        search_query=search_query,
    )
    return paginated_messages

@contact_bp.route("/archivar/", methods=["POST"])
@check_user_permissions(permissions_required=["mensaje_destroy"])
@inject
def logical_delete_message(
    contact_repository: AbstractContactRepository = Provide[Container.contact_repository]
):
    """
    Archive a message.

    Args:
        contact_repository (AbstractContactRepository): The repository for contact data.

    Returns:
        A redirect to the message's detail page with a flash message indicating success or failure.
    """
    message_id = request.form["message_id"]
    archived = contact_repository.logical_delete_message(message_id)

    if not archived:
        flash("El mensaje no existe o no ha podido ser archivado, intentelo nuevamente", "warning")
    else:
        flash("El mensaje ha sido archivado correctamente", "success")
    return redirect(url_for("contact_bp.show_message", message_id=message_id))

@contact_bp.route("/recuperar/", methods=["POST"])
@check_user_permissions(permissions_required=["mensaje_destroy"])
@inject
def recover_message(
    contact_repository: AbstractContactRepository = Provide[Container.contact_repository]
):
    """
    Recover an archived message.

    Args:
        contact_repository (AbstractContactRepository): The repository for contact data.

    Returns:
        A redirect to the message's detail page with a flash message indicating success or failure.
    """
    message_id = request.form["message_id"]
    recovered = contact_repository.recover(message_id)

    if not recovered:
        flash("El mensaje no existe o no ha podido ser recuperado, intentelo nuevamente", "warning")
    else:
        flash("El mensaje ha sido recuperado correctamente", "success")
    return redirect(url_for("contact_bp.show_message", message_id=message_id))

@contact_bp.route("/delete/", methods=["POST"])
@check_user_permissions(permissions_required=["mensaje_destroy"])
@inject
def delete_message(
    contact_repository: AbstractContactRepository = Provide[Container.contact_repository]
):
    """
    Delete a message.

    Args:
        contact_repository (AbstractContactRepository): The repository for contact data.

    Returns:
        A redirect to the list of messages with a flash message indicating success or failure.
    """
    message_id = request.form["message_id"]
    deleted = contact_repository.delete(message_id)

    if not deleted:
        flash("El mensaje no ha podido ser eliminado, intentelo nuevamente", "danger")
    else:
        flash("El mensaje ha sido eliminado correctamente", "success")
    return redirect(url_for("contact_bp.get_messages"))