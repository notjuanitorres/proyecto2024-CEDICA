from .index import index_bp
from .auth import auth_bp
from .user import users_bp
from .employee import employee_bp
from .equestrian import equestrian_bp
from .payment import payment_bp
from .charges import charges_bp
from .jockey_amazon import jockey_amazon_bp
from .publications import publications_bp

__all__ = [
    "index_bp",
    "auth_bp",
    "users_bp",
    "employee_bp",
    "equestrian_bp",
    "payment_bp",
    "publications_bp",
    "charges_bp",
    "jockey_amazon_bp",
]
