from src.web.helpers import auth as auth_helper
from src.web.controllers import user, auth, employee, equestrian, charges
from src.core.module.accounts import validators
from src.web.controllers import user, auth, employee, equestrian
from src.core.module.user import validators
from .container import Container


container = Container()


def init_wiring():
    container.wire(modules=[
        # Add controllers or modules that are using Provide or @inject
        user,
        auth,
        charges,
        employee,
        equestrian,
        user,
        auth_helper,
        validators,
    ])
    container.init_resources()
