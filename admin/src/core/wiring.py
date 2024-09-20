from src.web.controllers import user, auth
from .container import Container

container = Container()

def init_wiring():
    # Add controllers or modules that are using Provide or @inject
    container.wire(modules=[user, auth])
    container.init_resources()

