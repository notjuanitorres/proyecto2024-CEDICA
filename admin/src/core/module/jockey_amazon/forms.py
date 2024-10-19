from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField, IntegerField, DateField, FormField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from src.core.module.jockey_amazon.models import FileTagEnum
from src.core.module.common.forms import AddressForm, PhoneForm, EmergencyContactForm, DocumentsSearchForm, \
    BaseManageDocumentsForm
from src.core.module.jockey_amazon.models import (
    DisabilityDiagnosisEnum, DisabilityTypeEnum, FamilyAssignmentEnum, PensionEnum, WorkProposalEnum, WorkConditionEnum, SedeEnum, DayEnum, EducationLevelEnum
)


def enum_choices(enum):
    return [(choice.name, choice.value) for choice in enum]

class SchoolInstitutionForm(FlaskForm):
    school_name = StringField('Nombre', validators=[DataRequired(), Length(max=200)])
    street = StringField('Calle', validators=[DataRequired(), Length(max=50)])
    number = IntegerField('Número', validators=[DataRequired()])
    department = StringField('Departamento', validators=[Optional(), Length(max=50)])
    locality = StringField('Localidad', validators=[DataRequired(), Length(max=50)])
    province = StringField('Provincia', validators=[DataRequired(), Length(max=50)])
    phone_country_code = StringField('Código de País', validators=[DataRequired(), Length(max=5)])
    phone_area_code = StringField('Código de Área', validators=[DataRequired(), Length(max=5)])
    phone_number = StringField('Número de Teléfono', validators=[DataRequired(), Length(max=15)])

class FamilyMemberForm(FlaskForm):
    relationship = StringField('Relación', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    dni = StringField('DNI', validators=[DataRequired(), Length(min=8, max=8)])
    street = StringField('Calle', validators=[DataRequired(), Length(max=50)])
    number = IntegerField('Número', validators=[DataRequired()])
    department = StringField('Departamento', validators=[Optional(), Length(max=50)])
    locality = StringField('Localidad', validators=[DataRequired(), Length(max=50)])
    province = StringField('Provincia', validators=[DataRequired(), Length(max=50)])
    phone_country_code = StringField('Código de País', validators=[DataRequired(), Length(max=5)])
    phone_area_code = StringField('Código de Área', validators=[DataRequired(), Length(max=5)])
    phone_number = StringField('Número de Teléfono', validators=[DataRequired(), Length(max=15)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Length(max=100)])
    education_level = SelectField('Nivel Educativo', choices=enum_choices(EducationLevelEnum), validators=[DataRequired()])
    occupation = StringField('Ocupación', validators=[DataRequired(), Length(max=100)])

class WorkAssignmentForm(FlaskForm):
    proposal = SelectField('Propuesta de Trabajo', choices=enum_choices(WorkProposalEnum), validators=[DataRequired()])
    condition = SelectField('Condición', choices=enum_choices(WorkConditionEnum), validators=[DataRequired()])
    sede = SelectField('Sede', choices=enum_choices(SedeEnum), validators=[DataRequired()])
    days = SelectField('Días', choices=enum_choices(DayEnum), validators=[DataRequired()])
    professor_or_therapist_id = IntegerField('ID del Profesor o Terapeuta', validators=[DataRequired()])
    conductor_id = IntegerField('ID del Conductor', validators=[DataRequired()])
    track_assistant_id = IntegerField('ID del Asistente de Pista', validators=[DataRequired()])
    horse_id = IntegerField('ID del Caballo', validators=[DataRequired()])

class JockeyAmazonManagementForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    dni = StringField('DNI', validators=[DataRequired(), Length(min=8, max=8)])
    birth_date = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    birthplace = StringField('Lugar de Nacimiento', validators=[DataRequired(), Length(max=100)])
    address = FormField(AddressForm)
    phone = FormField(PhoneForm)
    emergency_contact = FormField(EmergencyContactForm)
    has_scholarship = BooleanField('¿Está becado?')
    scholarship_observations = TextAreaField('Observaciones sobre la Beca', validators=[Optional()])
    scholarship_percentage = FloatField('Porcentaje de Beca', validators=[Optional()])
    has_disability = BooleanField('¿Posee Certificado de Discapacidad?')
    disability_diagnosis = SelectField('Diagnóstico', choices=enum_choices(DisabilityDiagnosisEnum), validators=[Optional()])
    disability_other = StringField('Otro diagnóstico', validators=[Optional(), Length(max=100)])
    disability_type = SelectField('Tipo de Discapacidad', choices=enum_choices(DisabilityTypeEnum), validators=[Optional()])
    has_family_assignment = BooleanField('¿Percibe alguna Asignación Familiar?')
    family_assignment_type = SelectField('Tipo de Asignación Familiar', choices=enum_choices(FamilyAssignmentEnum), validators=[Optional()])
    has_pension = BooleanField('¿Posee alguna Pensión?')  # Checkbox
    pension_type = SelectField('Tipo de Pensión', choices=[(choice.name, choice.value) for choice in PensionEnum], validators=[Optional()])
    pension_details = StringField('Detalles de la Pensión', validators=[Optional(), Length(max=100)])
    social_security = StringField('Obra Social del Alumno', validators=[Optional(), Length(max=100)])
    social_security_number = StringField('Número de Afiliado', validators=[Optional(), Length(max=50)])
    has_curatorship = BooleanField('¿Posee curatela?')
    curatorship_observations = TextAreaField('Observaciones sobre la Curatela', validators=[Optional()])
    school_institution = FormField(SchoolInstitutionForm)
    current_grade_year = StringField('Grado / Año Actual', validators=[Optional(), Length(max=50)])
    school_observations = TextAreaField('Observaciones sobre la Institución Escolar', validators=[Optional()])
    professionals = TextAreaField('Profesionales que lo atienden', validators=[Optional()])
    family_member1 = FormField(FamilyMemberForm)
    family_member2 = FormField(FamilyMemberForm)
    work_assignments = FormField(WorkAssignmentForm)

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        
        if not self.family_member1.first_name.data:
            self.family_member1.first_name.errors.append('Este campo es obligatorio.')
            return False
        
        return True


class JockeyAmazonCreateForm(JockeyAmazonManagementForm):
    pass

class JockeyAmazonEditForm(JockeyAmazonManagementForm):
    def __init__(self, *args, **kwargs):
        super(JockeyAmazonEditForm, self).__init__(*args, **kwargs)
        self.current_dni = kwargs.pop('current_dni', None)

class JockeyAmazonSearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_by = SelectField(
        choices=[
            ('first_name', 'Nombre'),
            ('last_name', 'Apellido'),
            ('dni', 'DNI'),
            ('professionals', 'Profesionales que lo atienden'),
        ],
        validate_choice=True,
    )
    search_text = StringField(validators=[Length(max=50)])
    order_by = SelectField(
        choices=[
            ('inserted_at', 'Fecha de creación'),
            ('first_name', 'Nombre'),
            ('last_name', 'Apellido'),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[
            ('asc', 'Ascendente'),
            ('desc', 'Descendente'),
        ],
        validate_choice=True,
    )
    submit_search = SubmitField("Buscar")


class JockeyAmazonAddDocumentsForm(BaseManageDocumentsForm):
    tag = SelectField(
        "Tag",
        choices=[(e.name, e.value) for e in FileTagEnum],
        validators=[
            DataRequired(
                message="Debe seleccionar lo que representa este archivo",
            )
        ],
    )


class JockeyAmazonDocumentSearchForm(DocumentsSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_tag.choices = [
            ("", "Ver Todos"),
        ] + [(e.name, e.value) for e in FileTagEnum]
