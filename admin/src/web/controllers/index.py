from flask import Blueprint, render_template, redirect, request, flash, session, url_for

from src.core.module.auth import AbstractAuthServices
from src.core.container import Container
from dependency_injector.wiring import inject, Provide

index_bp = Blueprint("index_bp", __name__, template_folder="../templates", url_prefix="/")


@index_bp.route("/")
def index():
    """
    Renders the home page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template("index.html")


@index_bp.route("/home")
def home():
    """
    Renders the home page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template("home.html")


@index_bp.route("/descargar-documento")
@inject
def download_url(storage_services=Provide[Container.storage_services],
                 auth_services: AbstractAuthServices = Provide[Container.auth_services]):
    """
    Generates and redirects to a presigned download URL for a file.

    Retrieves the file path from the query parameters, generates a presigned download URL
    using the storage service, and redirects to the download URL. If the file path is not
    provided or the URL cannot be generated, the user is redirected back with an error message.

    Args:
        storage_services (AbstractStorageServices): The storage service for managing files.
            This is injected automatically using dependency injection.
        auth_services (AbstractAuthServices): The authentication service for managing users.

    Returns:
        Response: Redirects to the presigned URL or the referrer with a flash message on error.
    """
    return_url = request.referrer or "/"
    path = request.args.get("path")

    if not auth_services.has_permissions(user_id=session.get("user"),
                                         permissions_required=["ecuestre_show", "equipo_show", "jya_show"]):
        flash("No tienes permisos para descargar archivos", "danger")
        return redirect(url_for("index_bp.home"))

    url = storage_services.presigned_download_url(path)
    if not path or not url:
        flash("No se pudo descargar el archivo", "danger")
        return redirect(return_url)

    return redirect(url)
