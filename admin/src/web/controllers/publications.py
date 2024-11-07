from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from dependency_injector.wiring import inject, Provide

from src.core.module.publication.mappers import PublicationMapper
from src.core.module.user import AbstractUserRepository
from src.core.module.publication.forms import PublicationSearchForm, PublicationCreateForm, PublicationEditForm
from src.core.module.publication import PublicationRepository, AbstractPublicationRepository
from src.web.helpers.auth import check_user_permissions
from src.core.container import Container

publications_bp = Blueprint(
    "publications_bp", __name__, template_folder="../templates/publication", url_prefix="/publicaciones"
)


@publications_bp.route("/", methods=["GET", "POST"])
@check_user_permissions(permissions_required=['publicaciones_index'])
@inject
def get_publications(
    publication_repository: PublicationRepository = Provide[Container.publication_repository],
):
    """
    Route to get a paginated list of publications.

    Args:
        publication_repository (publicationRepository): The publication repository.

    Returns:
        Response: The rendered template for the list of publications (str).
    """
    form = PublicationSearchForm(request.args)
    search_query: dict = {}
    order_by = []
    if form.submit_search.data and form.validate():
        search_query = {"text": form.search_text.data, "field": form.search_by.data, "filters": {}}

        if form.start_date.data and form.end_date.data:
            search_query["filters"]["start_date"] = form.start_date.data
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

    return render_template("./publication/publications.html", search_form=form, publications=publications)


@publications_bp.route("/archivar/", methods=["POST"])
@check_user_permissions(permissions_required=["publicaciones_destroy"])
@inject
def archive_publication(
        publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository],
):
    """
    Route to archive a publication.

    Args:
        publication_repository (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: Redirect to the publication details.
    """
    publication_id = request.form["item_id"]
    archived = publication_repository.archive_publication(int(publication_id))
    if not archived:
        flash("La publicación no existe o ya ha sido archivada", "warning")
    else:
        flash("La publicación ha sido archivada correctamente", "success")
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
    recovered = publications.recover_publication(int(publication_id))
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
    user_repository: AbstractUserRepository = Provide[Container.user_repository],
):
    """
    Route to show details of a specific publication.

    Args:
        publication_id (int): The ID of the publication.
        publication_repository (AbstractPublicationsRepository): The publication repository.
        user_repository (AbstractUserRepository): The user repository.

    Returns:
        Response: The rendered template for the publication details if the publication exists,
         otherwise redirect to the list of publications.
    """
    publication = publication_repository.get_by_id(publication_id)
    if not publication:
        flash(f"La publicación con ID = {publication_id} no existe", "danger")
        return get_publications()

    author = user_repository.get_user(publication.get("author_id"))
    return render_template('./publication/publication.html', publication=publication, author=author)


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

    if publication.get("is_archived"):
        flash("No se puede editar una publicación archivada", "danger")
        return redirect(url_for("publications_bp.show_publication", publication_id=publication_id))

    edit_form = PublicationEditForm(data=publication)

    if request.method in ["POST", "PUT"]:
        return update_publication(publication_id=publication_id, edit_form=edit_form)

    return render_template("./publication/edit_publication.html", form=edit_form, publication=publication)


@inject
def update_publication(
    publication_id: int,
    edit_form: PublicationEditForm,
    publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository]
):
    """
    Helper function to update a publication's details.

    Args:
        publication_id (int): The ID of the publication.
        edit_form (PublicationEditForm): The form for editing a publication.
        publication_repository (AbstractPublicationsRepository): The publication repository.

    Returns:
        Response: The rendered template for editing a publication if the form wasn't valid
         or redirect to publication details.
    """
    if not edit_form.validate_on_submit():
        return render_template("./publication/edit_publication.html", form=edit_form)

    publication_repository.update_publication(
        publication_id=publication_id,
        data=PublicationMapper.from_edit_form(edit_form.data),
    )

    flash("Publicación actualizada con éxito", "success")
    return redirect(url_for("publications_bp.show_publication", publication_id=publication_id))


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
        flash("La publicación no ha podido ser eliminada, inténtelo nuevamente", "danger")
    else:
        flash("La publicación ha sido eliminada correctamente", "success")

    return redirect(url_for("publications_bp.get_publications"))
