from wtforms.validators import ValidationError


class EmailExistence(object):
    """
    Validator to check if an email is already used by another user.

    Attributes:
        current_email (str): The current email of the user being edited.
        message (str): The error message to raise if validation fails.
    """

    def __init__(self, current_email: str = None, message=None):
        """
        Initialize the EmailExistence validator.

        Args:
            current_email (str, optional): The current email of the user being edited.
            message (str, optional): The error message to raise if validation fails.
        """
        self.current_email = current_email
        if not message:
            message = "Email is used"
        self.message = message

    def __call__(self, form, email):
        """
        Validate the email field.

        Args:
            form: The form object that includes the field.
            email: The field object representing the email input.

        Raises:
            ValidationError: If the email is already used by another user.
        """
        is_edit = form.current_email is not None
        is_user = email.data == form.current_email
        if is_edit and is_user:
            return
        
        service = self.import_validator()
        if service.validate_email(email=email.data):
            raise ValidationError(self.message)

    def import_validator(self):
        """
        Import the validator dynamically at runtime.

        Returns:
            The auth services container.
        """
        # Needed to import the container dynamically at run time
        # It is in order to work along with WTForms instantiation at definition
        # pylint: disable="C0415"
        from src.core.container import Container

        container = Container()
        return container.auth_services()