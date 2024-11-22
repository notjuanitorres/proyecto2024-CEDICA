from src.web.helpers import auth as auth_helper
from src.web.controllers import (
    user,
    auth,
    employee,
    equestrian,
    index,
    payment,
    charges,
    jockey_amazon,
    publications,
    contact
)
from src.web.controllers.jockey_and_amazon import update_jockey_amazon, create_jockey_amazon
from src.web.controllers.api import contact as contact_api, publications as publications_api
from src.core.module.user import validators
from .container import Container


container = Container()


def init_wiring():
    """
    Initialize the dependency injection wiring for the application.

    This function wires the specified modules and initializes the resources
    in the dependency injection container.

    Modules to wire:
        - index
        - user
        - auth
        - employee
        - equestrian
        - charges
        - jockey_amazon
        - create_jockey_amazon
        - update_jockey_amazon
        - validators
        - payment
        - auth_helper
        - publications
        - contact
        - api

    Returns:
        None
    """
    container.wire(
        modules=[
            # Add controllers or modules that are using Provide or @inject
            index,
            user,
            auth,
            employee,
            equestrian,
            charges,
            jockey_amazon,
            create_jockey_amazon,
            update_jockey_amazon,
            validators,
            payment,
            auth_helper,
            publications,
            contact,
            publications_api,
            contact_api
        ]
    )
    container.init_resources()
