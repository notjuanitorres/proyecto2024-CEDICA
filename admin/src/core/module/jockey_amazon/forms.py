"""
forms.py

This module defines various forms used in the jockey and amazon management system, including forms
for creating, editing, and searching jockeys and amazons, as well as handling their documents.
It leverages WTForms and Flask-WTF for form handling and validation.
"""

from typing import Dict
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
    TextAreaField,
    DateField,
    FormField,
    FloatField,
    SubmitField,
    HiddenField,
    FieldList,
)
from wtforms.validators import DataRequired, Length, Optional
from src.core.module.common.forms import (
    AddressForm,
    PhoneForm,
    EmergencyContactForm,
    DocumentsSearchForm,
    BaseManageDocumentsForm, CustomFloatField,
)
from src.core.module.common.validators import IsNumber
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
from .validators import DniExistence


def dni_existence(form, field):
    """Check if the DNI already exists in another jockey or amazon.

       Args:
        form: The form object that includes the field.
        field: The field object representing the DNI input.

    The validator ensures unique DNI numbers across all jockeys and amazons in the system.
    """
    validator = DniExistence(message="DNI en uso")
    validator(form, field)


class GeneralInformationForm(FlaskForm):
    """
    Form for collecting and managing general information about a jockey or amazon.

    This form handles basic personal information including identification, contact details,
    and emergency contact information.

    Fields:
        id (HiddenField): The unique identifier for the jockey/amazon
        first_name (StringField): First name of the jockey/amazon
        last_name (StringField): Last name of the jockey/amazon
        dni (StringField): National identification number
        birth_date (DateField): Date of birth
        birthplace (StringField): Place of birth
        address (FormField): Nested form for address information
        phone (FormField): Nested form for phone contact details
        emergency_contact (FormField): Nested form for emergency contact information
    """
    def __init__(self, *args, **kwargs):
        """Initialize the form with the current DNI for validation purposes."""
        super(GeneralInformationForm, self).__init__(*args, **kwargs)
        self.current_dni = kwargs.pop("current_dni", None)

    id = HiddenField("id")
    first_name = StringField("Nombre", validators=[
        DataRequired(message="El nombre es requerido"),
        Length(max=100, message="El nombre no puede superar los 100 caracteres")
    ])
    last_name = StringField("Apellido", validators=[
        DataRequired(message="El apellido es requerido"),
        Length(max=100, message="El apellido no puede superar los 100 caracteres")
    ])
    dni = StringField("DNI", validators=[
        DataRequired(message="El DNI es requerido"),
        Length(min=8, max=8, message="El DNI debe tener exactamente 8 caracteres"),
        dni_existence
    ])
    birth_date = DateField("Fecha de Nacimiento", validators=[
        DataRequired(message="La fecha de nacimiento es requerida")
    ])
    birthplace = StringField("Lugar de Nacimiento", validators=[
        DataRequired(message="El lugar de nacimiento es requerido"),
        Length(max=100, message="El lugar de nacimiento no puede superar los 100 caracteres")
    ])
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
    """
    Form for managing family-related information and benefits for a jockey or amazon.

    This form collects information about family assignments, pensions, and family members.
    It supports up to two family member entries and validates their information accordingly.

    Fields:
        has_family_assignment (BooleanField): Indicates if they receive family assignments
        family_assignment_type (SelectField): Type of family assignment received
        has_pension (BooleanField): Indicates if they receive a pension
        pension_type (SelectField): Type of pension received
        pension_details (StringField): Additional details about the pension
        family_members (FieldList): List of family member form entries
    """

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
    pension_details = StringField("Detalles de la Pensión", validators=[
        Optional(),
        Length(max=100, message="Los detalles de la pensión no pueden superar los 100 caracteres")
    ])
    family_members = FieldList(FormField(FamilyMemberForm), min_entries=2, max_entries=2)
    submit = SubmitField("Actualizar Informacion Familiar", name="family_submit")

    def validate(self, extra_validators=None):
        # Run default validation first
        super().validate(extra_validators)
        first_has_errors = self.family_members[0].errors
        if first_has_errors:
            return False
        second_member = self.family_members[1]
        if second_member.data.get("is_optional"):
            second_member.errors.clear()
            return True
        if not second_member.validate():
            return False
        
        return True

    def family_info_to_flat(self):
        """
        Converts the nested form data into a flat dictionary structure.
        
        Returns:
            dict: A flat dictionary containing all form fields with properly prefixed keys.
            Format:
            {
                'has_family_assignment': bool,
                'family_assignment_type': str,
                'has_pension': bool,
                'pension_type': str,
                'pension_details': str,
                'family_members: list[Dict]
            }
        """
        
        flat_data = {
            'has_family_assignment': self.has_family_assignment.data,
            'family_assignment_type': self.family_assignment_type.data if self.has_family_assignment.data else None,
            'has_pension': self.has_pension.data,
            'pension_type': self.pension_type.data if self.has_pension.data else None,
            'pension_details': self.pension_details.data if self.has_pension.data else None,
            'family_members': [member for member in self.family_members.data]
        }
        return flat_data


class HealthInformationForm(FlaskForm):
    """
    Form for managing health-related information and disability status.

    This form handles information about disabilities, medical coverage, and curatorship
    details for jockeys and amazons.

    Fields:
        has_disability (BooleanField): Indicates if they have a disability certificate
        disability_diagnosis (SelectField): Diagnosis classification
        disability_other (StringField): Other disability details if applicable
        disability_type (SelectField): Type of disability
        social_security (StringField): Healthcare provider information
        social_security_number (StringField): Healthcare membership number
        has_curatorship (BooleanField): Indicates if they have a legal guardian
        curatorship_observations (TextAreaField): Additional curatorship details
    """

    has_disability = BooleanField("¿Posee Certificado de Discapacidad?")
    disability_diagnosis = SelectField(
        "Diagnóstico",
        choices=enum_choices(DisabilityDiagnosisEnum),
        validators=[Optional()],
    )
    disability_other = StringField("Otro diagnóstico", validators=[
        Optional(),
        Length(max=100, message="El diagnóstico no puede superar los 100 caracteres")
    ])

    disability_type = SelectField(
        "Tipo de Discapacidad",
        choices=enum_choices(DisabilityTypeEnum),
        validators=[Optional()],
    )
    social_security = StringField("Obra Social del Alumno", validators=[
        Optional(),
        Length(max=100, message="La obra social no puede superar los 100 caracteres")
    ])
    social_security_number = StringField("Número de Afiliado", validators=[
        Optional(),
        Length(max=50, message="El número de afiliado no puede superar los 50 caracteres")
    ])
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
    """
    Form for managing educational information for jockeys and amazons.

    This form collects information about their current educational institution,
    academic progress, and any relevant observations.

    Fields:
        school_institution (FormField): Nested form for school details
        current_grade_year (StringField): Current academic grade or year
        school_observations (TextAreaField): Additional observations about schooling
    """

    school_institution = FormField(SchoolInstitutionForm)
    current_grade_year = StringField("Grado / Año Actual", validators=[
        Optional(),
        Length(max=50, message="El grado/año no puede superar los 50 caracteres")
    ])
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
    """
    Form for managing work assignments and scholarship information.

    This form handles information about scholarships, professional support,
    and specific work assignments within the organization.

    Fields:
        has_scholarship (BooleanField): Indicates if they receive a scholarship
        scholarship_observations (TextAreaField): Additional scholarship details
        scholarship_percentage (CustomFloatField): Scholarship coverage percentage
        professionals (TextAreaField): Information about supporting professionals
        work_assignments (FormField): Nested form for specific work assignments
    """

    # Scholarship information
    has_scholarship = BooleanField("¿Está becado?")
    scholarship_observations = TextAreaField(
        "Observaciones sobre la Beca", validators=[Optional()]
    )
    scholarship_percentage = CustomFloatField("Porcentaje de Beca", validators=[Optional()])
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
    """
    Base form for managing all aspects of a jockey or amazon's information.

    This form combines all sub-forms into a comprehensive management interface,
    including general, family, health, educational, and work-related information.

    Fields:
        general_information (FormField): Personal and contact information
        family_information (FormField): Family-related details and benefits
        health_information (FormField): Health and disability information
        school_information (FormField): Educational details
        organization_information (FormField): Work and scholarship information
    """
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
    """
    Form for creating a new jockey or amazon record.

    Extends the management form to handle the specific requirements of creating
    a new record in the system.
    """
    pass


class JockeyAmazonEditForm(JockeyAmazonManagementForm):
    """
    Form for editing an existing jockey or amazon record.

    Extends the management form to handle the specific requirements of updating
    an existing record, including validation against current data.

    Additional attributes:
        current_email: Stores the current email for validation purposes
        current_dni: Stores the current DNI for validation purposes
    """
    def __init__(self, *args, **kwargs):
        super(JockeyAmazonEditForm, self).__init__(*args, **kwargs)
        self.current_email = kwargs.pop("current_email", None)
        self.current_dni = kwargs.pop("current_dni", None)


class JockeyAmazonSearchForm(FlaskForm):
    """
    Form for searching jockey and amazon records.

    Provides various search criteria and ordering options for finding specific records
    in the system.

    Fields:
        search_by (SelectField): Field to search by (name, lastname, DNI, professionals)
        search_text (StringField): Text to search for
        filter_debtors (BooleanField): Filter for jockeys/amazons with debts
        order_by (SelectField): Field to order results by
        order (SelectField): Sort order (ascending/descending)
    """

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

    filter_debtors = SelectField(
        "Deudores",
        choices=[("", "Ver Todos"), ("True", "Con deuda"), ("False", "Sin deuda"),],
        validate_choice=True,
    )
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
    """
    Form for adding documents to a jockey or amazon's record.

    Extends the base documents form to include specific document tagging
    for jockey/amazon-related files.

    Fields:
        tag (SelectField): Classification tag for the uploaded document
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


class JockeyAmazonDocumentSearchForm(DocumentsSearchForm):
    """
    Form for searching documents associated with jockeys and amazons.

    Extends the base document search form to include specific filtering
    options for jockey/amazon document types.

    Fields:
        filter_tag (SelectField): Filter for specific document types
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_tag.choices = [
            ("", "Ver Todos"),
        ] + [(e.name, e.value) for e in FileTagEnum]


class JockeyAmazonSelectForm(FlaskForm):
    """
    Form for selecting a specific jockey or amazon from a list.

    Used when associating a jockey or amazon with other entities in the system.

    Fields:
        selected_jya (HiddenField): ID of the selected jockey/amazon
        submit_jya (SubmitField): Button to confirm the selection
    """

    selected_item = HiddenField(
        "Empleado seleccionado",
        validators=[DataRequired("Se debe seleccionar un empleado"), IsNumber()],
    )
    submit_jya = SubmitField("Asociar")

    def set_selected_jya(self, account_id):
        self.selected_item.data = account_id


class JockeyAmazonMiniSearchForm(FlaskForm):
    """
    Form for quick search functionality of jockeys and amazons.

    Provides a simplified search interface for finding jockeys and amazons
    by basic criteria.

    Fields:
        search_text (StringField): Text to search for
        submit_search (SubmitField): Button to submit the search
    """
    search_text = StringField(
        validators=[Length(message="Debe ingresar un texto entre 1 y 50 caracteres", min=1, max=50)]
    )
    submit_search = SubmitField("Buscar")
