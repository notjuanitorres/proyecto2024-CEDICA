from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    BooleanField,
    SelectField,
    DateField,
    SubmitField,
    HiddenField
)
from wtforms.validators import DataRequired, Length
from src.core.module.common.validators import IsNumber
from src.core.module.common import IsValidName
from src.core.module.common.forms import BaseSearchForm, BaseManageDocumentsForm, DocumentsSearchForm
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
        validate_choice=True,
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
            DataRequired(message="Debe ingresar un nombre"),
            Length(max=100, message="El nombre no puede tener más de 100 caracteres"),
            IsValidName(),
        ],
    )

    breed = StringField(
        "Raza",
        validators=[
            DataRequired(message="Debe ingresar una raza"),
            Length(max=100, message="La raza no puede tener más de 100 caracteres"),
        ],
    )

    birth_date = DateField(
        "Fecha de nacimiento",
        validators=[
            DataRequired(message="Debe ingresar una fecha de nacimiento"),
        ],
    )

    sex = SelectField(
        "Sexo",
        choices=[("M", "Macho"), ("H", "Hembra")],
        validators=[
            DataRequired(message="Debe seleccionar un sexo"),
        ],
        validate_choice=True,
    )

    coat = StringField(
        "Pelaje",
        validators=[
            DataRequired(message="Debe ingresar un pelaje"),
            Length(max=100, message="El pelaje no puede tener más de 100 caracteres"),
        ],
    )

    is_donation = BooleanField("Es donación", default=False)

    admission_date = DateField(
        "Fecha de ingreso",
        validators=[
            DataRequired(message="Debe ingresar una fecha de ingreso"),
        ],
    )

    assigned_facility = StringField(
        "Facilidad asignada",
        validators=[
            DataRequired(message="Debe ingresar una facilidad asignada"),
            Length(max=100, message="La facilidad asignada no puede tener más de 100 caracteres"),
        ],
    )

    ja_type = SelectField(
        "Tipo de J&A asignado",
        choices=[(jtype.name, jtype.value) for jtype in JAEnum],
        validators=[
            DataRequired(message="Debe seleccionar un tipo de J&A"),
        ],
        validate_choice=True,
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


class HorseAssignSearchForm(FlaskForm):
    """
    Form for searching horses to assign to a jockey.

    Attributes:
        search_text (StringField): The text to search for.
        filter_activity (SelectField): The filter for activity type.
        submit_search (SubmitField): The search button.
    """
    search_text = StringField(
        "Buscar por nombre, email o dni"
    )
    filter_activity = SelectField(
        "Actividad Asignada",
        choices=[("", "Ver Todos")] + [(jtype.name, jtype.value) for jtype in JAEnum],
        validate_choice=True,
    )
    submit_search = SubmitField("Buscar")


class HorseAssignSelectForm(FlaskForm):
    """
    Form for selecting a horse from a list

    Attributes:
        selected_item (HiddenField): The selected horse id.
        submit_horse (SubmitField): The button to submit the search.
    """
    selected_item = HiddenField(
        "Caballo seleccionado",
        validators=[DataRequired("Se debe seleccionar un caballo"), IsNumber()],
    )
    submit_horse = SubmitField("Asociar")
