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
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def validate(self, form, extra_validators=[]):
        if not super().validate(form, extra_validators):
            return False
        
        if not self.data or len(self.data) == 0:
            self.errors.append("Debe seleccionar al menos un día")
            return False
            
        return True


def enum_choices(enum, first_value: tuple[str, str] = None):
    if first_value:
        return [first_value] + [(choice.name, choice.value) for choice in enum]
    return [(choice.name, choice.value) for choice in enum]


class SchoolInstitutionForm(FlaskForm):
    class Meta:
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
