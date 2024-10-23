from flask_wtf import FlaskForm
from flask_wtf.file import FileSize, FileAllowed
from wtforms import RadioField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL
from wtforms.fields import (
    IntegerField,
    StringField,
    TelField,
)
from .validators import IsNumber


def max_file_size(size_in_mb: int):
    """
        Calculate the maximum file size in bytes.

        Args:
            size_in_mb (int): The size in megabytes.

        Returns:
            int: The size in bytes.
        """
    BYTES_PER_MB = 1024 * 1024

    size_in_bytes = size_in_mb * BYTES_PER_MB

    return size_in_bytes


class AddressForm(FlaskForm):
    """
    Form for entering address details.

    Attributes:
        street (StringField): The street name.
        number (IntegerField): The street number.
        department (StringField): The department name.
        locality (StringField): The locality name.
        province (StringField): The province name.
    """
    street = StringField("Calle", validators=[DataRequired(), Length(max=50)])
    number = IntegerField("Numero", validators=[DataRequired()])
    department = StringField("Departamento", validators=[Optional(), Length(max=50)])
    locality = StringField("Localidad", validators=[DataRequired(), Length(max=50)])
    province = StringField("Provincia", validators=[DataRequired(), Length(max=50)])


class PhoneForm(FlaskForm):
    """
    Form for entering phone details.

    Attributes:
        country_code (TelField): The country code.
        area_code (TelField): The area code.
        number (TelField): The phone number.
    """
    country_code = TelField(
        "Codigo de pais", validators=[DataRequired(), Length(max=5)]
    )
    area_code = TelField(
        "Codigo de area", validators=[DataRequired(), Length(max=5), IsNumber()]
    )
    number = TelField(
        "Numero", validators=[DataRequired(), Length(min=9, max=15), IsNumber()]
    )


class EmergencyContactForm(FlaskForm):
    """
    Form for entering emergency contact details.

    Attributes:
        emergency_contact_name (StringField): The name of the emergency contact.
        emergency_contact_phone (TelField): The phone number of the emergency contact.
    """
    emergency_contact_name = StringField(
        "Nombre contacto de emergencia", validators=[DataRequired(), Length(max=50)]
    )
    emergency_contact_phone = TelField(
        "Telefono contacto de emergencia", validators=[DataRequired()]
    )


allowed_filetypes = ["pdf", "jpg", "jpeg", "png", "webp"]
formatted_filetypes = ", ".join(f".{ext}" for ext in allowed_filetypes[:-1]) + f" y .{allowed_filetypes[-1]}"
filetypes_message = f"Formato no reconocido. Formato válido: {formatted_filetypes}"


class BaseManageDocumentsForm(FlaskForm):
    """
    Base form for managing documents.

    Attributes:
        upload_type (RadioField): The type of upload (file or URL).
        title (StringField): The title of the document.
        file (FileField): The file to be uploaded.
        url (StringField): The URL of the document.
    """
    upload_type = RadioField(
        'Tipo de subida',
        choices=[('file', 'Archivo'), ('url', 'URL')],
        validators=[DataRequired(message="Debe seleccionar el tipo de subida")],
        default='url',
        validate_choice=True
    )

    title = StringField(
        "Título",
        validators=[
            DataRequired(message="Debe proporcionar un título"),
            Length(max=100, message="El título no puede exceder los 100 caracteres")
        ]
    )

    file = FileField(
        "Archivo",
        validators=[
            Optional(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                upload_set=allowed_filetypes,
                message=filetypes_message,
            ),
        ]
    )

    url = StringField(
        'Url',
        validators=[
            Optional(),
            URL(message="Debe proporcionar una URL válida")
        ],
        default="https://ejemplo.com"
    )

    def validate(self, *args, is_file_already_uploaded: bool = False, **kwargs):
        """
        Validate the form.

        It checks that the file field is not empty when the upload type is 'file' and the file isn't already uploaded,
        and if the url field is empty when the upload type is 'url'.

        Args:
            is_file_already_uploaded (bool): Indicates if the file is already uploaded.

        Returns:
            bool: True if the form is valid, False otherwise.
        """
        if not super(BaseManageDocumentsForm, self).validate():
            return False

        if self.upload_type.data == 'file':
            if not self.file.data and not is_file_already_uploaded:
                self.file.errors.append('Debe adjuntar un archivo cuando selecciona "Archivo"')
                return False
        elif self.upload_type.data == 'url':
            if not self.url.data:
                self.url.errors.append('Debe proporcionar una URL cuando selecciona "URL"')
                return False

        return True


class BaseSearchForm(FlaskForm):
    """
    Base form for search functionality.

    Attributes:
        search_by (SelectField): The field to search by.
        search_text (StringField): The search text.
        order_by (SelectField): The field to order by.
        order (SelectField): The order direction (asc or desc).
        submit_search (SubmitField): The submit button for the search.
    """
    class Meta:
        csrf = False

    search_by = SelectField(
        choices=[],
        validate_choice=True,
    )

    search_text = StringField(validators=[Length(max=50)])

    order_by = SelectField(
        choices=[],
        validate_choice=True,
    )

    order = SelectField(
        choices=[("asc", "Ascendente"), ("desc", "Descendente")], validate_choice=True
    )
    submit_search = SubmitField("Buscar")


class DocumentsSearchForm(BaseSearchForm):
    """
    Form for searching documents.

    Attributes:
        filter_tag (SelectField): The filter for document tags.
    """
    def __init__(self, *args, **kwargs):
        """Initialize the form with search and order choices."""
        super().__init__(*args, **kwargs)
        self.search_by.choices = [
            ("title", "Título"),
        ]
        self.order_by.choices = [
            ("title", "Título"),
            ("inserted_at", "Fecha de subida"),
        ]

    filter_tag = SelectField(
        choices=[], validate_choice=True)
