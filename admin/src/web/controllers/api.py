from datetime import datetime

from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide

from src.core.container import Container
from src.core.module.publication import AbstractPublicationRepository
from src.core.module.publication.mappers import PublicationMapper

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")


@api_bp.route("/articles", methods=["GET"])
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

    publications = publication_repository.get_page(page, per_page, search_query)

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
