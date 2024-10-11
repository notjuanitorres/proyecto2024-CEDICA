from wtforms.validators import ValidationError


class FilesNumber(object):
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = f"Maximum number of files is {max} and the minimum {min}." % (
                min,
                max,
            )
        self.message = message

    def __call__(self, form, field):
        files = field.data

        if (self.min != -1 and len(files) < self.min) or (
            self.max != -1 and len(files) > self.max
        ):
            raise ValidationError(self.message)


class IsNumber(object):
    def __init__(self, message=None) -> None:
        if not message:
            message = "Debe ser un numero"
        self.message = message

    def __call__(self, form, field):
        if not field.data.isdigit():
            raise ValidationError(self.message)