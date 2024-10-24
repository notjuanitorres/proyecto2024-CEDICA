"""
validators.py

This module defines custom WTForms validators to check the existence of 
email and DNI (Documento Nacional de Identidad) in the repository.
"""

from wtforms.validators import ValidationError


class Validator(object):
    """
    Base class for custom validators that allows dynamic service import.

    Methods:
        import_services: Dynamically imports the employee repository
        from the service container.
    """

    def import_services(self):
        """Imports the dependency injector container at runtime"""
        # Needed to import the container dynamically at run time
        # It is in order to work along with WTForms instantiation at definition
        # pylint: disable="C0415"
        from src.core.container import Container

        container = Container()
        return container.employee_repository()


class EmailExistence(Validator):
    """
    Callable validator to check the uniqueness of an email address.

    Attributes:
        current_email (str): The email address currently associated
        with the user (if editing).
        message (str): The error message to display if the email
        already exists.

    Methods:
        __call__(form, email): Validates the email field against
        the existing records.
    """

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
    """
    Callable validator to check the uniqueness of a DNI.

    Attributes:
        current_dni (str): The DNI currently associated with the user
        (if editing).
        message (str): The error message to display if the DNI
        already exists.

    Methods:
        __call__(form, dni): Validates the DNI field against
        the existing records.
    """

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
