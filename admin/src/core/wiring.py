from src.web.helpers import auth as auth_helper
from src.web.controllers import user, auth, employee, equestrian, index, jockey_amazon
from src.web.controllers.jockey_and_amazon import create_jockey_amazon
from src.core.module.user import validators
from .container import Container


container = Container()


def init_wiring():
    container.wire(modules=[
        # Add controllers or modules that are using Provide or @inject
        index,
        user,
        auth,
        employee,
        equestrian,
        jockey_amazon,
        create_jockey_amazon,
        validators,
        auth_helper
    ])
    container.init_resources()
