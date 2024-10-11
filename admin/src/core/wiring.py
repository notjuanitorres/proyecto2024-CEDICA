from src.web.helpers import auth as auth_helper
from src.web.controllers import user, auth, employee, equestrian, payment
from src.core.module.accounts import validators
from .container import Container


container = Container()


def init_wiring():
    container.wire(modules=[
        # Add controllers or modules that are using Provide or @inject
        user,
        auth,
        employee,
        equestrian,
        validators,
        payment,
        auth_helper
    ])
    container.init_resources()
