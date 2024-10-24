from wtforms.validators import ValidationError


class Validator(object):
    def import_services(self):
        # Needed to import the container dynamically at run time
        # It is in order to work along with WTForms instantiation at definition
        # pylint: disable="C0415"
        from src.core.container import Container

        container = Container()
        return container.employee_repository()


class EmailExistence(Validator):
    def __init__(self, current_email: str = None, message=None):
        self.current_email = current_email
        if not message:
            message = "Email en uso"
        self.message = message

    def __call__(self, form, email):
        is_edit = form.current_email is not None
        is_user = email.data == form.current_email
        if is_edit and is_user:
            return

        repository = self.import_services()
        if repository.is_email_used(email=email.data):
            raise ValidationError(self.message)


class DniExistence(Validator):
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

        repository = self.import_services()
        if repository.is_dni_used(dni=dni.data):
            raise ValidationError(self.message)
