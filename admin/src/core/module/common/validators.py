from wtforms.validators import ValidationError


class FilesNumber(object):
    """
    Validator to check if the number of files in a field is within a specified range.

    Args:
        min (int, optional): Minimum number of files allowed. Defaults to -1 (no limit).
        max (int, optional): Maximum number of files allowed. Defaults to -1 (no limit).
        message (str, optional): Custom error message. If not provided, a default message is used.
    """

    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = f"Maximum number of files is {max} and the minimum {min}."
        self.message = message

    def __call__(self, form, field):
        """Validates the number of files in the field.

        Args:
            form (Form): The form containing the field.
            field (Field): The field to validate.

        Raises:
            ValidationError: If the number of files is outside the specified range.
        """
        files = field.data
        if files is None:
            files = []
        if (self.min != -1 and len(files) < self.min) or (
            self.max != -1 and len(files) > self.max
        ):
            raise ValidationError(self.message)


class IsNumber(object):
    """
    Validator to check if the field's value is a number.

    Args:
        message (str, optional): Custom error message. If not provided, a default message is used.
    """

    def __init__(self, message=None) -> None:
        if not message:
            message = "Debe ser un numero"
        self.message = message

    def __call__(self, form, field):
        """Validates that the field's data is a number.

        Args:
            form (Form): The form containing the field.
            field (Field): The field to validate.

        Raises:
            ValidationError: If the field's data is not a number.
        """
        if not field.data.isdigit():
            raise ValidationError(self.message)
