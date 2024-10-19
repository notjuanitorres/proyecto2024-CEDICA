from flask import Blueprint, render_template, redirect, request, flash
from src.core.container import Container
from dependency_injector.wiring import inject, Provide

index_bp = Blueprint("index_bp", __name__, template_folder="../templates", url_prefix="/")


@index_bp.route("/")
def home():
    """
    Renders the home page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template("home.html")


@index_bp.route("/descargar_url")
@inject
def download_url(storage_services=Provide[Container.storage_services]):
    """
    Generates and redirects to a presigned download URL for a file.

    Retrieves the file path from the query parameters, generates a presigned download URL
    using the storage service, and redirects to the download URL. If the file path is not
    provided or the URL cannot be generated, the user is redirected back with an error message.

    Args:
        storage_services (AbstractStorageServices): The storage service for managing files.
            This is injected automatically using dependency injection.

    Returns:
        Response: Redirects to the presigned URL or the referrer with a flash message on error.
    """
    path = request.args.get("path")
    if not path:
        flash("No se proporcionó una ruta de archivo", "error")
        return redirect(request.referrer)

    url = storage_services.presigned_download_url(path)
    if url is None:
        flash("No se pudo descargar el archivo", "error")
        return redirect(request.referrer)

    return redirect(url)
