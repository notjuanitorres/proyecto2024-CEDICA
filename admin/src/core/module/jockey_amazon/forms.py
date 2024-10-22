from typing import Dict
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
    TextAreaField,
    IntegerField,
    DateField,
    FormField,
    FloatField,
    SubmitField,
    HiddenField,
)
from wtforms.validators import DataRequired, Length, Optional
from src.core.module.common.forms import (
    AddressForm,
    PhoneForm,
    EmergencyContactForm,
    DocumentsSearchForm,
    BaseManageDocumentsForm,
)
from src.core.module.jockey_amazon.data import (
    DisabilityDiagnosisEnum,
    DisabilityTypeEnum,
    FamilyAssignmentEnum,
    PensionEnum,
    FileTagEnum,
)
from .extras.forms import (
    FamilyMemberForm,
    WorkAssignmentsForm,
    SchoolInstitutionForm,
    enum_choices,
)
from src.core.module.common.validators import IsNumber


class GeneralInformationForm(FlaskForm):
    id = HiddenField("id")
    first_name = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    last_name = StringField("Apellido", validators=[DataRequired(), Length(max=100)])
    dni = StringField("DNI", validators=[DataRequired(), Length(min=8, max=8)])
    birth_date = DateField("Fecha de Nacimiento", validators=[DataRequired()])
    birthplace = StringField(
        "Lugar de Nacimiento", validators=[DataRequired(), Length(max=100)]
    )
    address = FormField(AddressForm)
    phone = FormField(PhoneForm)
    emergency_contact = FormField(EmergencyContactForm)
    submit = SubmitField("Actualizar Informacion General", name="general_submit")

    @staticmethod
    def general_info_to_flat(general_form: "GeneralInformationForm") -> Dict:
        """Convert GeneralInformationForm data into a flat dictionary to match the model."""
        flat_data = {
            "first_name": general_form.first_name.data,
            "last_name": general_form.last_name.data,
            "dni": general_form.dni.data,
            "birth_date": general_form.birth_date.data,
            "birthplace": general_form.birthplace.data,
            "street": general_form.address.street.data,
            "number": general_form.address.number.data,
            "department": general_form.address.department.data,
            "locality": general_form.address.locality.data,
            "province": general_form.address.province.data,
            "country_code": general_form.phone.country_code.data,
            "area_code": general_form.phone.area_code.data,
            "phone": general_form.phone.number.data,
            "emergency_contact_name": general_form.emergency_contact.emergency_contact_name.data,
            "emergency_contact_phone": general_form.emergency_contact.emergency_contact_phone.data,
        }
        return flat_data


class FamilyInformationForm(FlaskForm):
    has_family_assignment = BooleanField("¿Percibe alguna Asignación Familiar?")
    family_assignment_type = SelectField(
        "Tipo de Asignación Familiar",
        choices=enum_choices(FamilyAssignmentEnum),
        validators=[Optional()],
    )
    has_pension = BooleanField("¿Posee alguna Pensión?")  # Checkbox
    pension_type = SelectField(
        "Tipo de Pensión",
        choices=[(choice.name, choice.value) for choice in PensionEnum],
        validators=[Optional()],
    )
    pension_details = StringField(
        "Detalles de la Pensión", validators=[Optional(), Length(max=100)]
    )
    family_member1 = FormField(FamilyMemberForm)
    family_member2 = FormField(FamilyMemberForm)
    submit = SubmitField("Actualizar Informacion Familiar", name="family_submit")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        if not self.family_member1.first_name.data:
            self.family_member1.first_name.errors.append("Este campo es obligatorio.")
            return False

        return True


class HealthInformationForm(FlaskForm):
    has_disability = BooleanField("¿Posee Certificado de Discapacidad?")
    disability_diagnosis = SelectField(
        "Diagnóstico",
        choices=enum_choices(DisabilityDiagnosisEnum),
        validators=[Optional()],
    )
    disability_other = StringField(
        "Otro diagnóstico", validators=[Optional(), Length(max=100)]
    )
    disability_type = SelectField(
        "Tipo de Discapacidad",
        choices=enum_choices(DisabilityTypeEnum),
        validators=[Optional()],
    )
    social_security = StringField(
        "Obra Social del Alumno", validators=[Optional(), Length(max=100)]
    )
    social_security_number = StringField(
        "Número de Afiliado", validators=[Optional(), Length(max=50)]
    )
    has_curatorship = BooleanField("¿Posee curatela?")
    curatorship_observations = TextAreaField(
        "Observaciones sobre la Curatela", validators=[Optional()]
    )
    submit = SubmitField("Actualizar Informacion de Salud", name="health_submit")

    @staticmethod
    def health_info_to_flat(form: "HealthInformationForm") -> dict:
        """
        Flattens the data from the HealthInformationForm into a dictionary.
        """
        return {
            "has_disability": form.has_disability.data,
            "disability_diagnosis": form.disability_diagnosis.data,
            "disability_other": form.disability_other.data,
            "disability_type": form.disability_type.data,
            "social_security": form.social_security.data,
            "social_security_number": form.social_security_number.data,
            "has_curatorship": form.has_curatorship.data,
            "curatorship_observations": form.curatorship_observations.data,
        }


class SchoolInformationForm(FlaskForm):
    school_institution = FormField(SchoolInstitutionForm)
    current_grade_year = StringField(
        "Grado / Año Actual", validators=[Optional(), Length(max=50)]
    )
    school_observations = TextAreaField(
        "Observaciones sobre la Institución Escolar", validators=[Optional()]
    )
    submit = SubmitField("Actualizar Informacion Escolar", name="school_submit")

    @staticmethod
    def school_info_to_flat(form: "SchoolInformationForm") -> dict:
        """
        Flattens the data from the SchoolInformationForm into a dictionary.
        """
        return {
            "school_institution": {
                "name": form.school_institution.school_name.data,
                "street": form.school_institution.street.data,
                "number": form.school_institution.number.data,
                "department": form.school_institution.department.data,
                "locality": form.school_institution.locality.data,
                "province": form.school_institution.province.data,
                "phone_country_code": form.school_institution.phone_country_code.data,
                "phone_area_code": form.school_institution.phone_area_code.data,
                "phone_number": form.school_institution.phone_number.data,
            },
            "current_grade_year": form.current_grade_year.data,
            "school_observations": form.school_observations.data,
        }


class WorkAssignmentForm(FlaskForm):
    # Scholarship information
    has_scholarship = BooleanField("¿Está becado?")
    scholarship_observations = TextAreaField(
        "Observaciones sobre la Beca", validators=[Optional()]
    )
    scholarship_percentage = FloatField("Porcentaje de Beca", validators=[Optional()])
    # Organization work
    professionals = TextAreaField(
        "Profesionales que lo atienden", validators=[Optional()]
    )
    work_assignments = FormField(WorkAssignmentsForm)
    submit = SubmitField("Actualizar Asignaciones Laborales", name="assignment_submit")

    @staticmethod
    def work_assignment_to_flat(form: "WorkAssignmentForm") -> dict:
        """
        Flattens the data from the WorkAssignmentForm into a dictionary.
        """
        return {
            "has_scholarship": form.has_scholarship.data,
            "scholarship_observations": form.scholarship_observations.data,
            "scholarship_percentage": form.scholarship_percentage.data,
            "professionals": form.professionals.data,
            "work_assignments": {
                "proposal": form.work_assignments.proposal.data,
                "condition": form.work_assignments.condition.data,
                "sede": form.work_assignments.sede.data,
                "days": form.work_assignments.days.data,
            },
        }


class JockeyAmazonManagementForm(FlaskForm):
    # General information
    general_information = FormField(GeneralInformationForm)
    # Family information
    family_information = FormField(FamilyInformationForm)
    # Health information
    health_information = FormField(HealthInformationForm)
    # Educational information
    school_information = FormField(SchoolInformationForm)
    # Work assignments information
    organization_information = FormField(WorkAssignmentForm)


class JockeyAmazonCreateForm(JockeyAmazonManagementForm):
    pass


class JockeyAmazonEditForm(JockeyAmazonManagementForm):
    def __init__(self, *args, **kwargs):
        super(JockeyAmazonEditForm, self).__init__(*args, **kwargs)
        self.current_email = kwargs.pop("current_email", None)
        self.current_dni = kwargs.pop("current_dni", None)


class JockeyAmazonSearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_by = SelectField(
        choices=[
            ("first_name", "Nombre"),
            ("last_name", "Apellido"),
            ("dni", "DNI"),
            ("professionals", "Profesionales que lo atienden"),
        ],
        validate_choice=True,
    )
    search_text = StringField(validators=[Length(max=50)])
    order_by = SelectField(
        choices=[
            ("inserted_at", "Fecha de creación"),
            ("first_name", "Nombre"),
            ("last_name", "Apellido"),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[
            ("asc", "Ascendente"),
            ("desc", "Descendente"),
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
        validate_choice=True,
    )


class JockeyAmazonDocumentSearchForm(DocumentsSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_tag.choices = [
            ("", "Ver Todos"),
        ] + [(e.name, e.value) for e in FileTagEnum]


class JockeyAmazonSelectForm(FlaskForm):
    selected_jya = HiddenField(
        "Empleado seleccionado",
        validators=[DataRequired("Se debe seleccionar un empleado"), IsNumber()],
    )
    submit_jya = SubmitField("Asociar")

    def set_selected_jya(self, account_id):
        self.selected_jya.data = account_id


class JockeyAmazonMiniSearchForm(FlaskForm):
    search_text = StringField(
        validators=[Length(message="Debe ingresar un texto", min=1, max=50)]
    )
    submit_search = SubmitField("Buscar")
