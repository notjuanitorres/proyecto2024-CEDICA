from datetime import datetime

from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide

from src.core.container import Container
from src.core.module.publication import AbstractPublicationRepository
from src.core.module.publication.mappers import PublicationMapper
from src.core.module.publication.models import EstadoPublicacionEnum

publications_api_bp = Blueprint("api_bp", __name__, url_prefix="/articles")


@publications_api_bp.route("/", methods=["GET"])
@inject
def get_publications_api(
    publication_repository: AbstractPublicationRepository = Provide[Container.publication_repository],
):
    """
    API route to get a paginated JSON list of articles.

    Args:
        publication_repository (PublicationRepository): The publication repository.

    Returns:
        Response: JSON response with the list of articles.
    """

    author = request.args.get("author")
    published_from = request.args.get("published_from")
    published_to = request.args.get("published_to")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    search_query = {"filters": {}}

    if author:
        search_query["text"] = author
        search_query["field"] = "alias"

    if published_from:
        try:
            search_query["filters"]["start_date"] = datetime.fromisoformat(published_from).date().isoformat()
        except ValueError:
            return jsonify({"error": "Invalid format for published_from"}), 400

    if published_to:
        try:
            search_query["filters"]["end_date"] = datetime.fromisoformat(published_to).date().isoformat()
        except ValueError:
            return jsonify({"error": "Invalid format for published_to"}), 400

    search_query["filters"]["status"] = EstadoPublicacionEnum.PUBLISHED.name
    publications = publication_repository.get_page(page, per_page, search_query, order_by=[("publish_date", "desc")])

    response_data = {
        "data": [
            PublicationMapper.to_api(publication)
            for publication in publications
        ],
        "page": page,
        "per_page": per_page,
        "total": publications.total,
    }

    return jsonify(response_data), 200


@publications_api_bp.route("/<int:publication_id>", methods=["GET"])
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
        Response: JSON response with the publication details.
    """
    try:
        publication_id = int(publication_id)
    except ValueError:
        return jsonify({"error": "Parámetros inválidos o faltantes en la solicitud."}), 400

    publication = publication_repository.get_by_id(publication_id)
    if (not publication
            or publication["is_deleted"]
            or not publication["status"] == EstadoPublicacionEnum.PUBLISHED.value):
        return jsonify({"error": "Publicación no encontrada"}), 404

    publication["author"] = publication["author"].alias
    return jsonify(publication), 200
