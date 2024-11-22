from flask import Blueprint
from . import contact, publications
from .contact import contact_api_bp
from .publications import publications_api_bp

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
api_bp.register_blueprint(contact_api_bp)
api_bp.register_blueprint(publications_api_bp)

__all__ = [
    "contact",
    "publications",
    "contact_api_bp",
    "publications_api_bp",
    "api_bp"
]