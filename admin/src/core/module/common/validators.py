from wtforms.validators import ValidationError

class IsNumber(object):
    def __init__(self, message=None) -> None:
        if not message:
            message = "Debe ser un numero"
        self.message = message

    def __call__(self, form, field):
        if not field.data.isdigit():
            raise ValidationError(self.message)