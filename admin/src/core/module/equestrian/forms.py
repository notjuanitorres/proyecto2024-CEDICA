from flask_wtf import FlaskForm
from flask_wtf.file import FileSize, FileAllowed, FileRequired
from wtforms.fields import (
    StringField,
    BooleanField,
    SelectField,
    DateField,
    SelectMultipleField,
    SubmitField, FileField, MultipleFileField, FormField,
)
from wtforms.validators import DataRequired, Length, Optional, URL
from wtforms import widgets, RadioField

from src.core.module.common import (
    FilesNumber,
    max_file_size,
)
from src.core.module.equestrian.models import JAEnum, Horse, FileTagEnum


class MultiCheckboxField(SelectMultipleField):
    """
    https://wtforms.readthedocs.io/en/3.0.x/specific_problems/?highlight=listwidget#specialty-field-tricks
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


allowed_filetypes = ["pdf", "doc", "xls", "jpg", "jpeg", "png", "webp"]
formatted_filetypes = ", ".join(f".{ext}" for ext in allowed_filetypes[:-1]) + f" y .{allowed_filetypes[-1]}"
filetypes_message = f"Formato no reconocido. Formato válido: {formatted_filetypes}"


class HorseDocumentsForm(FlaskForm):
    ficha_general = MultipleFileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                allowed_filetypes,
                message=filetypes_message,
            ),
            FilesNumber(min=0, max=5, message="Puede subir hasta 5 archivos"),
        ]
    )
    planificacion_entrenamiento = MultipleFileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                allowed_filetypes,
                message=filetypes_message,
            ),
            FilesNumber(min=0, max=5, message="Puede subir hasta 5 archivos"),
        ]
    )
    informe_evolucion = MultipleFileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                allowed_filetypes,
                message=filetypes_message,
            ),
            FilesNumber(min=0, max=5, message="Puede subir hasta 5 archivos"),
        ]
    )
    carga_imagenes = MultipleFileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                allowed_filetypes,
                message=filetypes_message,
            ),
            FilesNumber(min=0, max=10, message="Puede subir hasta 10 archivos"),
        ]
    )
    registro_veterinario = MultipleFileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                allowed_filetypes,
                message=filetypes_message,
            ),
            FilesNumber(min=0, max=5, message="Puede subir hasta 5 archivos"),
        ]
    )


class HorseAddDocumentsForm(FlaskForm):
    upload_type = RadioField(
        'Tipo de subida',
        choices=[('file', 'Archivo'), ('url', 'URL')],
        validators=[DataRequired(message="Debe seleccionar el tipo de subida")]
    )

    tag = SelectField(
        "Tag",
        choices=[(e.name, e.value) for e in FileTagEnum],
        validators=[
            DataRequired(
                message="Debe seleccionar lo que representa este archivo",
            )
        ],
    )

    title = StringField(
        "Título",
        validators=[
            DataRequired(message="Debe proporcionar un título"),
            Length(max=100, message="El título no puede exceder los 100 caracteres")
        ]
    )

    file = FileField(
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
        'URL',
        validators=[
            Optional(),
            URL(message="Debe proporcionar una URL válida")
        ]
    )

    def validate(self, *args, **kwargs):
        if not super(HorseAddDocumentsForm, self).validate():
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


class HorseManagementForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
    )

    breed = StringField(
        "Raza",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
    )

    birth_date = DateField(
        "Fecha de nacimiento",
        validators=[
            DataRequired(),
        ],
    )

    sex = SelectField(
        "Sexo",
        choices=[("M", "Macho"), ("H", "Hembra")],
        validators=[
            DataRequired(),
        ],
    )

    coat = StringField(
        "Pelaje",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
    )

    is_donation = BooleanField("Es donación", default=False)

    admission_date = DateField(
        "Fecha de ingreso",
        validators=[
            DataRequired(),
        ],
    )

    assigned_facility = StringField(
        "Facilidad asignada",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
    )

    ja_type = SelectField(
        "Tipo de J&A asignado",
        choices=[(jtype.name, jtype.value) for jtype in JAEnum],
        validators=[
            DataRequired(),
        ],
    )

    documents = FormField(HorseDocumentsForm)


class HorseCreateForm(HorseManagementForm):
    pass


class HorseEditForm(HorseManagementForm):
    def __init__(self, *args, **kwargs):
        super(HorseEditForm, self).__init__(*args, **kwargs)
        self.trainers.choices = self.get_trainers_choices()

    def import_services(self):
        # Needed to import the container dynamically at run time
        # It is in order to work along with WTForms instantiation at definition
        # pylint: disable="C0415"
        from src.core.container import Container

        container = Container()
        return container.employee_repository()

    def get_trainers_choices(self):
        return [
            (trainer.id, f"{trainer.fullname} ({trainer.position.value})")
            for trainer in self.import_services().get_trainers()
        ]

    trainers = MultiCheckboxField(
        "Entrenadores y conductores",
        choices=[],
    )


class HorseSearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_by = SelectField(
        choices=[
            ("name", "Nombre"),
        ],
        validate_choice=True,
    )
    search_text = StringField(validators=[Length(max=50)])

    filter_ja_type = SelectField(
        choices=[("", "Ver Todos")] + [(jtype.name, jtype.value) for jtype in JAEnum],
        validate_choice=True,
    )
    order_by = SelectField(
        choices=[
            ("id", "ID"),
            ("name", "Nombre"),
            ("birth_date", "Fecha de nacimiento"),
            ("admission_date", "Fecha de ingreso"),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[("asc", "Ascendente"), ("desc", "Descendente")], validate_choice=True
    )
    submit_search = SubmitField("Buscar")

