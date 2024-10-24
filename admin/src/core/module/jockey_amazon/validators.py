from wtforms.validators import ValidationError

class DniExistence(object):
    """
    Validator for checking whether a DNI (national ID) is already in use.

    Args:
        current_dni (str, optional): The current DNI of the entity being edited. Defaults to None.
        message (str, optional): Custom error message for the validator. Defaults to "DNI en uso".
    """

    def __init__(self, current_dni: str = None, message=None):
        """
        Initializes the DniExistence validator.

        Args:
            current_dni (str, optional): The current DNI if editing an existing entity. Defaults to None.
            message (str, optional): Error message to raise if the DNI is found in use. Defaults to "DNI en uso".
        """
        self.current_dni = current_dni
        if not message:
            message = "DNI en uso"
        self.message = message

    def __call__(self, form, dni):
        """
        Validates the DNI field of the form. If the form is for an existing entity and the DNI matches the current DNI,
        validation passes. Otherwise, it checks if the DNI is already in use.

        Args:
            form (Form): The WTForms form that is being validated.
            dni (Field): The DNI field to validate.

        Raises:
            ValidationError: If the DNI is already in use.
        """
        is_edit = form.current_dni is not None
        dni_owned = dni.data == form.current_dni
        if is_edit and dni_owned:
            return

        repository = self.import_services().jockey_amazon_repository()
        if repository.is_dni_used(dni=dni.data):
            raise ValidationError(self.message)
    
    def import_services(self):
        """
        Dynamically imports the necessary services (in this case, the `JockeyAmazonRepository`)
        to perform the validation.

        Returns:
            Container: The application's container that holds the repository services.
        """
        from src.core.container import Container

        container = Container()
        return container
