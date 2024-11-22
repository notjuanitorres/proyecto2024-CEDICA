from wtforms.validators import ValidationError, Regexp
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
        """Initializes the validator.

        Args:
            min (int, optional): Minimum number of files allowed. Defaults to -1 (no limit).
            max (int, optional): Maximum number of files allowed. Defaults to -1 (no limit).
            message (str, optional): Custom error message. If not provided, a default message is used
        """
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
        """
        Initializes the validator.

        Args:
            message (str, optional): Custom error message. If not provided, a default message is used.
        """
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
        """
        Initializes the validator.

        Args:
            message (str, optional): Custom error message. If not provided, a default message is used.
        """
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
        """
        Initializes the validator.

        Args:
            message (str, optional): Custom error message. If not provided, a default message is used.
        """
        if not message:
            message = "El DNI debe tener 8 dígitos"
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
        # - Longitud de 8 dígitos
        patron = r'^\d{8}$'

        if not re.match(patron, value):
            raise ValidationError(self.message)


class IsValidUrlHost(object):
    """
    Validator to check if the field's value is a valid URL host.

    Args:
        message (str, optional): Custom error message. If not provided, a default message is used.
    """

    def __init__(self, message=None) -> None:
        """
        Initializes the validator.

        Args:
            message (str, optional): Custom error message. If not provided, a default message is used.
        """
        if not message:
            message = "Ingrese una URL válida"
        self.message = message

    def __call__(self, form, field):
        """Validates that the field's data is a valid URL.

        Args:
            form (Form): The form containing the field.
            field (Field): The field to validate.

        Raises:
            ValidationError: If the field's data is not a valid URL.
        """
        if not field.data:
            raise ValidationError("El campo no puede estar vacío")

        value = str(field.data).strip()

        # Patrón que acepta:
        # - Protocolo http o https
        # - Dominio
        # - Ruta
        # - Parámetros de consulta
        # - Fragmento
        patron = r''

        if not re.match(patron, value):
            raise ValidationError(self.message)


class URLWithoutProtocol(Regexp):
    """
    Regex-based URL validation that disregards the protocol.

    :param require_tld:
        If true, the domain-name portion of the URL must contain a .tld
        suffix. Set to false to allow domains like `localhost`.
    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, require_tld=True, message=None):
        regex = (
            r"^(?P<host>[^\/\?:]+)"
            r"(?P<port>:[0-9]+)?"
            r"(?P<path>\/.*?)?"
            r"(?P<query>\?.*)?$"
        )
        super().__init__(regex, re.IGNORECASE, message)
        self.validate_hostname = HostnameValidation(
            require_tld=require_tld
        )

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext("Invalid URL.")

        match = super().__call__(form, field, message)
        if not self.validate_hostname(match.group("host")):
            raise ValidationError(message)


class HostnameValidation:
    """
    Helper class for checking hostnames for validation.

    This is not a validator in and of itself, and as such is not exported.
    """

    hostname_part = re.compile(r"^(xn-|[a-z0-9_]+)(-[a-z0-9_-]+)*$", re.IGNORECASE)
    tld_part = re.compile(r"^([a-z]{2,20}|xn--([a-z0-9]+-)*[a-z0-9]+)$", re.IGNORECASE)

    def __init__(self, require_tld=True):
        self.require_tld = require_tld

    def __call__(self, hostname):
        # Encode out IDNA hostnames. This makes further validation easier.
        try:
            hostname = hostname.encode("idna")
        except UnicodeError:
            pass

        # Turn back into a string in Python 3x
        if not isinstance(hostname, str):
            hostname = hostname.decode("ascii")

        if len(hostname) > 253:
            return False

        # Check that all labels in the hostname are valid
        parts = hostname.split(".")
        for part in parts:
            if not part or len(part) > 63:
                return False
            if not self.hostname_part.match(part):
                return False

        if self.require_tld and (len(parts) < 2 or not self.tld_part.match(parts[-1])):
            return False

        return True
