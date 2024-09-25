from src.web.controllers import user, auth
from src.core.module.accounts import validators
from .container import Container

container = Container()


def init_wiring():
    # Add controllers or modules that are using Provide or @inject
    container.wire(modules=[user, auth, validators])
    container.init_resources()

