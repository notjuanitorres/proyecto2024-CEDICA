from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from dependency_injector.wiring import inject, Provide

from src.core.module.publication.mappers import PublicationMapper
from src.core.module.publication.forms import PublicationSearchForm, PublicationCreateForm, PublicationEditForm
from src.core.module.publication import PublicationRepository, AbstractPublicationRepository
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container
import nh3

publications_bp = Blueprint(
    "publications_bp", __name__, template_folder="../templates/publication", url_prefix="/publicaciones"
)


@publications_bp.route("/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['publicaciones_index'])
@inject
def get_publications(
    publication_repository: PublicationRepository = Provide[Container.publication_repository],
    deleted: bool = False
):
    """
    Route to get a paginated list of publications.

    Args:
        publication_repository (publicationRepository): The publication repository.
        deleted (bool): Flag to indicate if the list of publications to retrieve are logically deleted.

    Returns:
        Response: The rendered template for the list of publications (str).
    """

    if request.args.get("deleted") is not None:
        deleted = request.args.get("deleted") == "True"

    form = PublicationSearchForm(request.args)
    search_query: dict = {"filters": {"is_deleted": deleted}}
    order_by = []
    if form.submit_search.data and form.validate():
        search_query["text"] = form.search_text.data
        search_query["field"] = form.search_by.data

        if form.start_date.data:
            search_query["filters"]["start_date"] = form.start_date.data
        if form.end_date.data:
            search_query["filters"]["end_date"] = form.end_date.data

        if form.filter_type.data:
            search_query["filters"]["type"] = form.filter_type.data

        if form.filter_status.data:
            search_query["filters"]["status"] = form.filter_status.data

        if form.order_by.data and form.order.data:
            order_by = [(form.order_by.data, form.order.data)]

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    publications = publication_repository.get_page(page, per_page, search_query, order_by)

    return render_template("./publication/publications.html",
                           search_form=form, publications=publications, are_deleted=deleted)


@publications_bp.route("/archivar/", methods=["POST"])
@check_user_permissions(permissions_required=["publicaciones_destroy"])
@inject
def logical_delete_publication(
        publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository],
):
    """
    Route to logically delete a publication.

    Args:
        publication_repository (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: Redirect to the publication details.
    """
    publication_id = request.form["item_id"]
    try:
        publication_id = int(publication_id)
    except ValueError:
        flash("La publicación solicitada no existe", "danger")
        return redirect(url_for("publications_bp.get_publications"))

    try:
        deleted = publication_repository.logical_delete_publication(publication_id)
    except ValueError:
        flash("No se puede eliminar una publicación con estado 'publicada'."
              " Debe ser despublicada primero.", "warning")
        return redirect(url_for("publications_bp.show_publication", publication_id=publication_id))

    if not deleted:
        flash("La publicación no existe o ya ha sido eliminada", "warning")
    else:
        flash("La publicación ha sido eliminada correctamente", "success")
    return redirect(url_for("publications_bp.show_publication", publication_id=publication_id))


@publications_bp.route("/recuperar/", methods=["POST"])
@check_user_permissions(permissions_required=["publicaciones_destroy"])
@inject
def recover_publication(
        publications: AbstractPublicationRepository = Provide[Container.publication_repository],
):
    """
    Route to recover a publication.

    Args:
        publications (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: Redirect to the publication details.
    """
    publication_id = request.form["publication_id"]
    try:
        publication_id = int(publication_id)
    except ValueError:
        flash("La publicación solicitada no existe", "danger")
        return redirect(url_for("publications_bp.get_publications"))

    recovered = publications.recover_publication(publication_id)
    if not recovered:
        flash("La publicación no existe o no puede ser recuperada", "warning")
    else:
        flash("La publicación ha sido recuperada correctamente", "success")
    return redirect(url_for("publications_bp.show_publication", publication_id=publication_id))


@publications_bp.route("/<int:publication_id>")
@check_user_permissions(permissions_required=["publicaciones_show"])
@inject
def show_publication(
    publication_id: int,
    publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository],
):
    """
    Route to show details of a specific publication.

    Args:
        publication_id (int): The ID of the publication.
        publication_repository (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: The rendered template for the publication details if the publication exists,
         otherwise redirect to the list of publications.
    """
    publication = publication_repository.get_by_id(publication_id)
    if not publication:
        flash(f"La publicación con ID = {publication_id} no existe", "danger")
        return get_publications()

    return render_template('./publication/publication.html',
                           publication=publication, author=publication["author"])


@publications_bp.route("/crear", methods=["GET", "POST"])
@check_user_permissions(permissions_required=["publicaciones_new"])
def create_publication():
    """
    Route to create a new publication.

    Returns:
        Response: The rendered template for creating a publication.
    """
    create_form = PublicationCreateForm()

    if request.method == "POST":
        return add_publication(create_form=create_form)

    return render_template("./publication/create_publication.html", form=create_form)


@inject
def add_publication(
    create_form: PublicationCreateForm,
    publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository]
):
    """
    Helper function to add a new publication.

    Args:
        create_form (PublicationCreateForm): The form for creating a publication.
        publication_repository (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: The rendered template for creating a publication if the form wasn't valid
         or redirect to publication details.
    """
    if not create_form.validate_on_submit():
        return render_template("./publication/create_publication.html", form=create_form)

    data = PublicationMapper.from_create_form(create_form.data)
    data["author_id"] = session.get("user")
    publication = publication_repository.add_publication(PublicationMapper.to_entity(data))

    flash("Publicación creada con éxito!", "success")
    return redirect(url_for("publications_bp.show_publication", publication_id=publication["id"]))


@publications_bp.route("/publicar-despublicar/<int:publication_id>", methods=["GET"])
@inject
def toggle_publication_status(
    publication_id: int,
    publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository]
):
    publication = publication_repository.get_by_id(publication_id)
    if not publication:
        flash(f"Hubo un error al cambiar el estado de esta publicación", "danger")
        return redirect(url_for("publications_bp.get_publications"))

    if publication.get("is_deleted"):
        flash("No se puede modificar una publicación eliminada", "danger")
        return redirect(url_for("publications_bp.show_publication", publication_id=publication_id))

    success = publication_repository.toggle_publication_status(publication_id)
    if not success:
        flash("Hubo un error al cambiar el estado de esta publicación", "danger")
    else:
        flash("Publicación actualizada con éxito", "success")

    return redirect(url_for("publications_bp.show_publication", publication_id=publication_id))


@publications_bp.route("/editar/<int:publication_id>", methods=["GET", "POST", "PUT"])
@check_user_permissions(permissions_required=["publicaciones_update"])
@inject
def edit_publication(
    publication_id: int,
    publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository]
):
    """
    Route to edit a publication's details.

    Args:
        publication_id (int): The ID of the publication.
        publication_repository (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: The rendered template for editing a publication if the publication exists,
        otherwise redirect to the list of publications.
    """
    publication = publication_repository.get_by_id(publication_id)

    if not publication:
        flash(f"Su búsqueda no devolvió una publicación existente", "danger")
        return redirect(url_for("publications_bp.get_publications"))

    if publication.get("is_deleted"):
        flash("No se puede editar una publicación eliminada", "danger")
        return redirect(url_for("publications_bp.show_publication", publication_id=publication_id))

    publication["status"] = publication["status"].name
    publication["type"] = publication["type"].name
    edit_form = PublicationEditForm(data=publication)

    if request.method in ["POST", "PUT"]:
        return update_publication(publication=publication, edit_form=edit_form)

    return render_template("./publication/edit_publication.html", form=edit_form, publication=publication)


@inject
def update_publication(
    publication,
    edit_form: PublicationEditForm,
    publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository]
):
    """
    Helper function to update a publication's details.

    Args:
        publication: The ID of the publication.
        edit_form (PublicationEditForm): The form for editing a publication.
        publication_repository (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: The rendered template for editing a publication if the form wasn't valid
         or redirect to publication details.
    """
    if not edit_form.validate_on_submit():
        return render_template("./publication/edit_publication.html", form=edit_form, publication=publication)

    if edit_form.data.get("content"):
        edit_form.data["content"] = nh3.clean(edit_form.data["content"])
    publication_repository.update_publication(
        publication_id=publication["id"],
        data=PublicationMapper.from_edit_form(edit_form.data),
    )

    flash("Publicación actualizada con éxito", "success")
    return redirect(url_for("publications_bp.show_publication", publication_id=publication["id"]))


@publications_bp.route("/delete/", methods=["POST"])
@check_user_permissions(permissions_required=["publicaciones_destroy"])
@inject
def delete_publication(
    publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository]
):
    """
    Route to delete a publication.

    Args:
        publication_repository (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: Redirect to the list of publications.
    """
    publication_id = request.form["item_id"]
    try:
        publication_id = int(publication_id)
    except ValueError:
        flash("La publicación solicitada no existe", "danger")
        return redirect(url_for("publications_bp.get_publications"))

    deleted = publication_repository.delete_publication(publication_id)
    if not deleted:
        flash("La publicación no ha podido ser eliminada permanentemente, inténtelo nuevamente", "danger")
    else:
        flash("La publicación ha sido eliminada permanentemente de manera correcta", "success")

    return redirect(url_for("publications_bp.get_publications"))
