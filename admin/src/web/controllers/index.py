from flask import Blueprint, render_template, redirect, request, flash
from src.core.container import Container
from dependency_injector.wiring import inject, Provide

index_bp = Blueprint("index_bp", __name__, template_folder="../templates", url_prefix="/")


@index_bp.route("/")
def home():
    return render_template("home.html")


@index_bp.route("/descargar_url")
@inject
def download_url(storage_services=Provide[Container.storage_services]):
    path = request.args.get("path")
    if not path:
        flash("No se proporcionó una ruta de archivo", "error")
        return redirect(request.referrer)

    url = storage_services.presigned_download_url(path)
    if url is None:
        flash("No se pudo descargar el archivo", "error")
        return redirect(request.referrer)

    return redirect(url)
