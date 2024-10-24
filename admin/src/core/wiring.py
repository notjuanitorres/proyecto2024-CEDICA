from src.web.helpers import auth as auth_helper
from src.web.controllers import user, auth, employee, equestrian, index, payment, charges, jockey_amazon
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
        - validators
        - auth_helper

    Returns:
        None
    """
    container.wire(modules=[
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
    ])
    container.init_resources()
