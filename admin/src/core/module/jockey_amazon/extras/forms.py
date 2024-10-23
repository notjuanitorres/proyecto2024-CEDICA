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

    def validate(self, form, extra_validators = []):
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
    school_name = StringField("Nombre", validators=[DataRequired(), Length(max=200)])
    street = StringField("Calle", validators=[DataRequired(), Length(max=50)])
    number = IntegerField("Número", validators=[DataRequired()])
    department = StringField("Departamento", validators=[Optional(), Length(max=50)])
    locality = StringField("Localidad", validators=[DataRequired(), Length(max=50)])
    province = StringField("Provincia", validators=[DataRequired(), Length(max=50)])
    phone_country_code = StringField(
        "Código de País", validators=[DataRequired(), Length(max=5)]
    )
    phone_area_code = StringField(
        "Código de Área", validators=[DataRequired(), Length(max=5)]
    )
    phone_number = StringField(
        "Número de Teléfono", validators=[DataRequired(), Length(max=15)]
    )


class FamilyMemberForm(FlaskForm):
    class Meta:
        csrf = False
    is_optional = HiddenField("Es opcional", default=False)
    relationship = StringField("Relación", validators=[DataRequired(), Length(max=50)])
    first_name = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    last_name = StringField("Apellido", validators=[DataRequired(), Length(max=100)])
    dni = StringField("DNI", validators=[DataRequired(), Length(min=8, max=8)])
    street = StringField("Calle", validators=[DataRequired(), Length(max=50)])
    number = IntegerField("Número", validators=[DataRequired()])
    department = StringField("Departamento", validators=[Optional(), Length(max=50)])
    locality = StringField("Localidad", validators=[DataRequired(), Length(max=50)])
    province = StringField("Provincia", validators=[DataRequired(), Length(max=50)])
    phone_country_code = StringField(
        "Código de País", validators=[DataRequired(), Length(max=5)]
    )
    phone_area_code = StringField(
        "Código de Área", validators=[DataRequired(), Length(max=5)]
    )
    phone_number = StringField(
        "Número de Teléfono", validators=[DataRequired(), Length(max=15)]
    )
    email = StringField(
        "Correo Electrónico", validators=[DataRequired(), Length(max=100)]
    )
    education_level = SelectField(
        "Nivel Educativo",
        choices=enum_choices(EducationLevelEnum),
        validators=[DataRequired()],
    )
    occupation = StringField("Ocupación", validators=[DataRequired(), Length(max=100)])


class WorkAssignmentsForm(FlaskForm):
    class Meta:
        csrf = False
    proposal = SelectField(
        "Propuesta de Trabajo",
        choices=enum_choices(WorkProposalEnum),
        validators=[DataRequired()],
    )
    condition = SelectField(
        "Condición",
        choices=enum_choices(WorkConditionEnum),
        validators=[DataRequired()],
    )
    sede = SelectField(
        "Sede", choices=enum_choices(SedeEnum), validators=[DataRequired()]
    )
    days = MultipleCheckboxField(
        "Días", choices=enum_choices(DayEnum), validate_choice=True
    )
