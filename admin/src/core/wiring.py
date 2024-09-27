from src.web.controllers import user, auth, equestrian
from src.core.module.accounts import validators
from src.web.helpers import auth as auth_helper
from .container import Container

container = Container()


def init_wiring():
    # Add controllers or modules that are using Provide or @inject
    container.wire(modules=[user, auth, equestrian, validators, auth_helper])
    container.init_resources()

