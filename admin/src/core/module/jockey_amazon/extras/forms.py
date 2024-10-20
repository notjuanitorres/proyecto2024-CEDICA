from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    IntegerField,
)
from wtforms.validators import DataRequired, Length, Optional
from src.core.module.common.forms import (
    AddressForm,
    PhoneForm,
    EmergencyContactForm,
    DocumentsSearchForm,
    BaseManageDocumentsForm,
)
from src.core.module.jockey_amazon.models import (
    WorkProposalEnum,
    WorkConditionEnum,
    SedeEnum,
    DayEnum,
    EducationLevelEnum,
)


def enum_choices(enum):
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
    days = SelectField(
        "Días", choices=enum_choices(DayEnum), validators=[DataRequired()]
    )
    # professor_or_therapist_id = IntegerField(
    #     "ID del Profesor o Terapeuta", validators=[DataRequired()]
    # )
    # conductor_id = IntegerField("ID del Conductor", validators=[DataRequired()])
    # track_assistant_id = IntegerField(
    #     "ID del Asistente de Pista", validators=[DataRequired()]
    # )
    # horse_id = IntegerField("ID del Caballo", validators=[DataRequired()])
