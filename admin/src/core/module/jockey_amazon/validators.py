from wtforms.validators import ValidationError


class DniExistence(object):
    def __init__(self, current_dni: str = None, message=None):
        self.current_dni = current_dni
        if not message:
            message = "DNI en uso"
        self.message = message

    def __call__(self, form, dni):
        is_edit = form.current_dni is not None
        dni_owned = dni.data == form.current_dni
        if is_edit and dni_owned:
            return

        repository = self.import_services().jockey_amazon_repository()
        if repository.is_dni_used(dni=dni.data):
            raise ValidationError(self.message)
    
    def import_services(self):
        # Needed to import the container dynamically at run time
        # It is in order to work along with WTForms instantiation at definition
        # pylint: disable="C0415"
        from src.core.container import Container

        container = Container()
        return container