from flask import Blueprint, render_template

index_bp = Blueprint("index_bp", __name__, template_folder="../templates", url_prefix="/")


@index_bp.route("/")
def home():
    return render_template("home.html")
