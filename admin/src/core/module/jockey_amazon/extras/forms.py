from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    IntegerField,
    HiddenField,
    SelectMultipleField,
    widgets,
)
from wtforms.validators import DataRequired, Length, Optional

from src.core.module.common import IsNumber
from src.core.module.jockey_amazon.models import (
    WorkProposalEnum,
    WorkConditionEnum,
    SedeEnum,
    DayEnum,
    EducationLevelEnum,
)


class MultipleCheckboxField(SelectMultipleField):
    """
    A custom form field that renders as multiple checkboxes.
    Extends SelectMultipleField to provide checkbox-style multiple selection functionality.
    
    Attributes:
        widget: ListWidget instance that renders the field without prefix labels
        option_widget: CheckboxInput instance for individual checkbox rendering
    
    Methods:
        validate: Ensures at least one checkbox is selected
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def validate(self, form, extra_validators=[]):
        """Validate the form

        Besides from nomal chehcks, it also ensures that at least one checkbox is selected

        Args:
            form: The form instance to validate
            extra_validators: Additional validators to run
        """
        if not super().validate(form, extra_validators):
            return False
        
        if not self.data or len(self.data) == 0:
            self.errors.append("Debe seleccionar al menos un día")
            return False
            
        return True


def enum_choices(enum, first_value: tuple[str, str] = None):
    """
    Converts an Enum class into a list of tuples suitable for form choices.
    
    Args:
        enum: The Enum class to convert
        first_value: Optional tuple of (name, value) to prepend to choices
        
    Returns:
        list[tuple[str, str]]: List of (name, value) tuples for form choices
    """
    if first_value:
        return [first_value] + [(choice.name, choice.value) for choice in enum]
    return [(choice.name, choice.value) for choice in enum]


class SchoolInstitutionForm(FlaskForm):
    """
    Form for collecting school institution information.
    
    Fields:
        school_name (str): Name of the school institution (required, max 200 chars)
        street (str): Street address (required, max 50 chars)
        number (int): Street number (required)
        department (str): Department/unit number (optional, max 50 chars)
        locality (str): City/locality (required, max 50 chars)
        province (str): Province/state (required, max 50 chars)
        phone_country_code (str): Country code for phone (required, max 5 chars)
        phone_area_code (str): Area code for phone (required, max 5 chars)
        phone_number (str): Phone number (required, max 15 chars)
    
    Meta:
        csrf: CSRF protection disabled for this form
    """
    class Meta:
        """Metaclass disabling CSRF protection."""
        csrf = False

    school_name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(max=200, message="El nombre no puede superar los 200 caracteres")
        ]
    )
    street = StringField(
        "Calle", validators=[
            DataRequired(message="La calle es obligatoria"),
            Length(max=50, message="La calle no puede superar los 50 caracteres")
        ]
    )
    number = IntegerField(
        "Número",
        validators=[DataRequired(message="El número es obligatorio")
                    ]
    )
    department = StringField(
        "Departamento",
        validators=[
            Optional(),
            Length(max=50, message="El departamento no puede superar los 50 caracteres")
        ]
    )
    locality = StringField(
        "Localidad",
        validators=[
            DataRequired(message="La localidad es obligatoria"),
            Length(max=50, message="La localidad no puede superar los 50 caracteres")
        ]
    )
    province = StringField(
        "Provincia",
        validators=[
            DataRequired(message="La provincia es obligatoria"),
            Length(max=50, message="La provincia no puede superar los 50 caracteres")
        ]
    )
    phone_country_code = StringField(
        "Código de País", validators=[DataRequired(message="El código de país es obligatorio"),
                                      Length(max=5, message="El código de país no puede superar los 5 caracteres")]
    )
    phone_area_code = StringField(
        "Código de Área", validators=[DataRequired(message="El código de área es obligatorio"),
                                      Length(max=5, message="El código de área no puede superar los 5 caracteres")]
    )
    phone_number = StringField(
        "Número de Teléfono",
        validators=[DataRequired(message="El número de teléfono es obligatorio"),
                    Length(max=15, message="El número de teléfono no puede superar los 15 caracteres")
                    ]
    )


class FamilyMemberForm(FlaskForm):
    """
    Form for collecting family member information.
    
    Fields:
        is_optional (bool): Hidden field indicating if the family member is optional
        relationship (str): Relationship to the jockey (required, max 50 chars)
        first_name (str): First name (required, max 100 chars)
        last_name (str): Last name (required, max 100 chars)
        dni (str): National ID number (required, exactly 8 digits)
        street (str): Street address (required, max 50 chars)
        number (int): Street number (required)
        department (str): Department/unit number (optional, max 50 chars)
        locality (str): City/locality (required, max 50 chars)
        province (str): Province/state (required, max 50 chars)
        phone_country_code (str): Country code for phone (required, max 5 chars)
        phone_area_code (str): Area code for phone (required, max 5 chars)
        phone_number (str): Phone number (required, max 15 chars)
        email (str): Email address (required, max 100 chars)
        education_level (SelectField): Education level from EducationLevelEnum
        occupation (str): Current occupation (required, max 100 chars)
    
    Meta:
        csrf: CSRF protection disabled for this form
    """
    class Meta:
        csrf = False
    is_optional = HiddenField("Es opcional", default=False)
    relationship = StringField(
        "Relación",
        validators=[
            DataRequired("La relación es obligatoria"),
            Length(max=50, message="La relación no puede superar los 50 caracteres")
        ]
    )

    first_name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(max=100, message="El nombre no puede superar los 100 caracteres")
        ]
    )
    last_name = StringField(
        "Apellido",
        validators=[DataRequired(message="El apellido es obligatorio"),
                    Length(max=100, message="El apellido no puede superar los 100 caracteres")
                    ]
    )
    dni = StringField(
        "DNI",
        validators=[
            DataRequired(message="El DNI es obligatorio"),
            Length(min=8, max=8, message="El DNI debe tener 8 caracteres"),
            IsNumber("Debe ser un número de 8 digitos!")
        ]
    )
    street = StringField(
        "Calle",
        validators=[
            DataRequired(message="La calle es obligatoria"),
            Length(max=50, message="La calle no puede superar los 50 caracteres")
        ]
    )
    number = IntegerField(
        "Número",
        validators=[
            DataRequired(message="El número es obligatorio")
        ]
    )
    department = StringField(
        "Departamento",
        validators=[
            Optional(),
            Length(max=50, message="El departamento no puede superar los 50 caracteres")
        ]
    )
    locality = StringField(
        "Localidad",
        validators=[
            DataRequired(message="La localidad es obligatoria"),
            Length(max=50, message="La localidad no puede superar los 50 caracteres")
        ]
    )
    province = StringField(
        "Provincia",
        validators=[
            DataRequired(message="La provincia es obligatoria"),
            Length(max=50, message="La provincia no puede superar los 50 caracteres")
        ]
    )

    phone_country_code = StringField(
        "Código de País", validators=[DataRequired(message="El código de país es obligatorio"),
                                      Length(max=5, message="El código de país no puede superar los 5 caracteres")]
    )
    phone_area_code = StringField(
        "Código de Área", validators=[DataRequired(message="El código de área es obligatorio"),
                                      Length(max=5, message="El código de área no puede superar los 5 caracteres")]
    )
    phone_number = StringField(
        "Número de Teléfono",
        validators=[
            DataRequired(message="El número de teléfono es obligatorio"),
            Length(max=15, message="El número de teléfono no puede superar los 15 caracteres")
        ]
    )
    email = StringField(
        "Correo Electrónico",
        validators=[
            DataRequired(message="El correo electrónico es obligatorio"),
            Length(max=100, message="El correo electrónico no puede superar los 100 caracteres")
        ]
    )
    education_level = SelectField(
        "Nivel Educativo",
        choices=enum_choices(EducationLevelEnum),
        validators=[DataRequired(message="Debe seleccionar un nivel educativo")],
    )
    occupation = StringField(
        "Ocupación",
        validators=[
            DataRequired(message="La ocupación es obligatoria"),
            Length(max=100, message="La ocupación no puede superar los 100 caracteres")
        ]
    )


class WorkAssignmentsForm(FlaskForm):
    """
    Form for managing work assignments and preferences.
    
    Fields:
        proposal (SelectField): Work proposal type from WorkProposalEnum
        condition (SelectField): Work condition from WorkConditionEnum
        sede (SelectField): Work location/headquarters from SedeEnum
        days (MultipleCheckboxField): Working days selection from DayEnum
    
    Meta:
        csrf: CSRF protection disabled for this form
        
    Note:
        The days field requires at least one day to be selected for validation to pass
    """

    class Meta:
        csrf = False
    proposal = SelectField(
        "Propuesta de Trabajo",
        choices=enum_choices(WorkProposalEnum),
        validators=[DataRequired("Debe seleccionar una propuesta")],
    )
    condition = SelectField(
        "Condición",
        choices=enum_choices(WorkConditionEnum),
        validators=[DataRequired("Debe seleccionar una condición")],
    )
    sede = SelectField(
        "Sede", choices=enum_choices(SedeEnum), validators=[DataRequired("Debe seleccionar una sede")]
    )
    days = MultipleCheckboxField(
        "Días", choices=enum_choices(DayEnum), validate_choice=True
    )
