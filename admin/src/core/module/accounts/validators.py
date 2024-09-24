from wtforms.validators import ValidationError


class EmailExistence(object):
    def __init__(self, current_email: str = None, message=None):
        self.current_email = current_email
        if not message:
            message = "Email is used"
        self.message = message

    def __call__(self, form, email):
        is_edit = form.current_email is not None
        is_user = email.data == form.current_email
        if is_edit and is_user:
            return
        
        service = self.import_validator()
        if service.validate_email(email=email.data):
            raise ValidationError(self.message)

    def import_validator(self):
        # Needed to import the container dynamically at run time
        # It is in order to work along with WTForms instantiation at definition
        # pylint: disable="C0415"
        from src.core.container import Container

        container = Container()
        return container.accounts_services()
