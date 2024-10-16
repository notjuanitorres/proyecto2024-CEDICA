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
    BYTES_PER_MB = 1024 * 1024

    size_in_bytes = size_in_mb * BYTES_PER_MB

    return size_in_bytes


class AddressForm(FlaskForm):
    street = StringField("Calle", validators=[DataRequired(), Length(max=50)])
    number = IntegerField("Numero", validators=[DataRequired()])
    department = StringField("Departamento", validators=[Optional(), Length(max=50)])
    locality = StringField("Localidad", validators=[DataRequired(), Length(max=50)])
    province = StringField("Provincia", validators=[DataRequired(), Length(max=50)])


class PhoneForm(FlaskForm):
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
    emergency_contact_name = StringField(
        "Nombre contacto de emergencia", validators=[DataRequired(), Length(max=50)]
    )
    emergency_contact_phone = TelField(
        "Telefono contacto de emergencia", validators=[DataRequired()]
    )


allowed_filetypes = ["pdf", "jpg", "jpeg", "png", "webp"]
formatted_filetypes = ", ".join(f".{ext}" for ext in allowed_filetypes[:-1]) + f" y .{allowed_filetypes[-1]}"
filetypes_message = f"Formato no reconocido. Formato válido: {formatted_filetypes}"


class BaseAddDocumentsForm(FlaskForm):
    upload_type = RadioField(
        'Tipo de subida',
        choices=[('file', 'Archivo'), ('url', 'URL')],
        validators=[DataRequired(message="Debe seleccionar el tipo de subida")]
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
        ]
    )

    def validate(self, *args, **kwargs):
        if not super(BaseAddDocumentsForm, self).validate():
            return False

        if self.upload_type.data == 'file':
            if not self.file.data:
                self.file.errors.append('Debe adjuntar un archivo cuando selecciona "Archivo"')
                return False
        elif self.upload_type.data == 'url':
            if not self.url.data:
                self.url.errors.append('Debe proporcionar una URL cuando selecciona "URL"')
                return False

        return True


class BaseSearchForm(FlaskForm):
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
