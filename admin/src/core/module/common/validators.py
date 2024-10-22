from wtforms.validators import ValidationError
import re


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
            message = f"El máximo numero de archivos es {max} y el mínimo es {min}."
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


class IsValidName(object):
    """
    Validator to check if the field's value is a valid name.

    Args:
        message (str, optional): Custom error message. If not provided, a default message is used.
    """

    def __init__(self, message=None) -> None:
        if not message:
            message = "Debe ser un nombre válido"
        self.message = message

    def __call__(self, form, field):
        """Validates that the field's data is a valid name.

        Args:
            form (Form): The form containing the field.
            field (Field): The field to validate.

        Raises:
            ValidationError: If the field's data is not a valid name.
        """
        if not field.data:
            raise ValidationError("El campo no puede estar vacío")

        value = str(field.data).strip()

        # Patrón que acepta:
        # - Letras (a-z, A-Z)
        # - Vocales con tilde (á,é,í,ó,ú,Á,É,Í,Ó,Ú)
        # - Ñ,ñ
        # - Ü,ü (diéresis)
        # - Espacios entre palabras
        # - Apóstrofes para nombres como D'Alessandro
        # - Guiones para nombres compuestos
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+(?:[\s\'-][a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+)*$'

        if not re.match(patron, value):
            raise ValidationError(self.message)

        if len(value) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres")

        # Fuente: https://www.argentina.gob.ar/sites/default/files/infoleg/disp902-1-357258.pdf
        if len(value) > 35:
            raise ValidationError("El nombre no puede exceder los 35 caracteres")


class IsValidDniNumber(object):
    """
    Validator to check if the field's value is a valid DNI number.

    Args:
        message (str, optional): Custom error message. If not provided, a default message is used.
    """

    def __init__(self, message=None) -> None:
        if not message:
            message = "Debe ser un DNI válido"
        self.message = message

    def __call__(self, form, field):
        """Validates that the field's data is a valid DNI number.

        Args:
            form (Form): The form containing the field.
            field (Field): The field to validate.

        Raises:
            ValidationError: If the field's data is not a valid DNI number.
        """
        if not field.data:
            raise ValidationError("El campo no puede estar vacío")

        value = str(field.data).strip()

        # Patrón que acepta:
        # - Números (0-9)
        # - Longitud de 7 u 8 dígitos
        patron = r'^\d{7,8}$'

        if not re.match(patron, value):
            raise ValidationError(self.message)
