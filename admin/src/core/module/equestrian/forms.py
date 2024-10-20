from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    BooleanField,
    SelectField,
    DateField,
)
from wtforms.validators import DataRequired, Length

from src.core.module.common.forms import BaseSearchForm, DocumentsSearchForm
from src.core.module.common.forms import BaseManageDocumentsForm
from src.core.module.equestrian.models import JAEnum, FileTagEnum


class HorseAddDocumentsForm(BaseManageDocumentsForm):
    """
    Form for adding documents related to a horse.

    Attributes:
        tag (SelectField): The tag representing the document.
    """
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
    """
    Form for managing horse details.

    Attributes:
        name (StringField): The name of the horse.
        breed (StringField): The breed of the horse.
        birth_date (DateField): The birthdate of the horse.
        sex (SelectField): The sex of the horse.
        coat (StringField): The coat color of the horse.
        is_donation (BooleanField): Indicates if the horse is a donation.
        admission_date (DateField): The admission date of the horse.
        assigned_facility (StringField): The facility assigned to the horse.
        ja_type (SelectField): The type of J&A assigned to the horse.
    """
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


class HorseCreateForm(HorseManagementForm):
    """Form for creating a new horse entry."""
    pass


class HorseEditForm(HorseManagementForm):
    """
    Form for editing an existing horse entry.
    """
    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super(HorseEditForm, self).__init__(*args, **kwargs)


class HorseSearchForm(BaseSearchForm):
    """
    Form for searching horses.

    Attributes:
        filter_ja_type (SelectField): The filter for J&A type.
    """
    def __init__(self, *args, **kwargs):
        """Initialize the form with search and order choices."""
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
    """
    Form for searching horse documents.

    Attributes:
        filter_tag (SelectField): The filter for document tags.
    """
    def __init__(self, *args, **kwargs):
        """Initialize the form with filter tag choices."""
        super().__init__(*args, **kwargs)
        self.filter_tag.choices = [
            ("", "Ver Todos"),
        ] + [(e.name, e.value) for e in FileTagEnum]