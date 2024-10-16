from flask_wtf import FlaskForm
from flask_wtf.file import FileSize, FileAllowed
from wtforms.fields import (
    StringField,
    BooleanField,
    SelectField,
    DateField,
    SelectMultipleField,
    MultipleFileField, FormField,
)
from wtforms.validators import DataRequired, Length
from wtforms import widgets

from src.core.module.common.forms import BaseSearchForm, DocumentsSearchForm
from src.core.module.common.forms import BaseManageDocumentsForm, allowed_filetypes, filetypes_message
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


class HorseAddDocumentsForm(BaseManageDocumentsForm):
    tag = SelectField(
        "Tag",
        choices=[(e.name, e.value) for e in FileTagEnum],
        validators=[
            DataRequired(
                message="Debe seleccionar lo que representa este archivo",
            )
        ],
    )


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


class HorseSearchForm(BaseSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_by.choices = [
            ("name", "Nombre"),
        ]
        self.order_by.choices = [
            ("id", "ID"),
            ("name", "Nombre"),
            ("birth_date", "Fecha de nacimiento"),
            ("admission_date", "Fecha de ingreso"),
        ]

    filter_ja_type = SelectField(
        choices=[("", "Ver Todos")] + [(jtype.name, jtype.value) for jtype in JAEnum],
        validate_choice=True,
    )


class HorseDocumentSearchForm(DocumentsSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_tag.choices = [
            ("", "Ver Todos"),
        ] + [(e.name, e.value) for e in FileTagEnum]

