from flask import Blueprint, render_template, redirect, request, flash, url_for, session, Response
#import requests
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
    return render_template("home.html")


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
    Generates a presigned download URL for a file and downloads the file in it.

    Retrieves the file path from the query parameters, generates a presigned download URL
    using the storage service, and downloads the file in it. If the file path is not
    provided or the URL cannot be generated, the user is redirected back with an error message.

    Args:
        storage_services (AbstractStorageServices): The storage service for managing files.
            This is injected automatically using dependency injection.
        auth_services (AbstractAuthServices): The authentication service for managing users.

    Returns:
        Response: Download the file or redirect to the referrer or home page with a flash message on error.
    """
    return_url = request.referrer or "/"
    path = request.args.get("path")

    if not auth_services.has_permissions(user_id=session.get("user"),
                                         permissions_required=["ecuestre_show", "equipo_show", "jya_show"]):
        flash("No tienes permisos para descargar archivos", "danger")
        return redirect(url_for("index_bp.home"))

    if not path:
        flash("No se proporcionó una ruta de archivo", "danger")
        return redirect(return_url)

    url = storage_services.presigned_download_url(path)

    if not url:
        flash("No se pudo descargar el archivo", "danger")
        return redirect(return_url)

    response = requests.get(url, stream=True)
    if response.status_code != 200:
        flash("No se pudo descargar el archivo", "danger")
        return redirect(return_url)

    filename = path.split("/")[-1]
    filename = filename[32:]
    return Response(
        response.iter_content(chunk_size=8192),
        headers={
            'Content-Disposition': 'attachment; filename=' + filename,
            'Content-Type': response.headers.get('Content-Type', 'application/octet-stream')
        }
    )
