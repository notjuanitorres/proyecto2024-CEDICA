"""
forms.py

This module defines various forms used in the employee management system, including forms
for creating, editing, and searching employees, as well as handling employee documents.
It leverages WTForms and Flask-WTF for form handling and validation.
"""

from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.fields import (
    StringField,
    BooleanField,
    SelectField,
    FormField,
    DateField,
    TextAreaField,
    FileField,
    MultipleFileField,
    HiddenField,
)

from src.core.module.common.validators import IsValidDniNumber
from src.core.module.common import IsValidName
from src.core.module.common.forms import (
    filetypes_message,
    allowed_filetypes,
    BaseManageDocumentsForm,
    BaseSearchForm,
    DocumentsSearchForm,
)
from src.core.module.employee.data import (
    ProfessionsEnum,
    JobPositionEnum as PositionEnum,
    JobConditionEnum as ConditionEnum,
    FileTagEnum,
)
from src.core.module.employee.validators import EmailExistence, DniExistence
from src.core.module.common import (
    AddressForm,
    EmergencyContactForm,
    PhoneForm,
    FilesNumber,
    IsNumber,
    max_file_size,
)


def email_existence(form, field):
    """Check if the email is assigned to another employee.

    Args:
        form: The form object that includes the field.
        field: The field object representing the email input.
    """
    validator = EmailExistence(message="Email en uso")
    validator(form, field)


def dni_existence(form, field):
    """Check if the DNI already exists in other employee.

    Args:
        form: The form object that includes the field.
        field: The field object representing the DNI input.
    """
    validator = DniExistence(message="DNI en uso")
    validator(form, field)


class EmploymentInformationForm(FlaskForm):
    """
    Form for collecting employment information of an employee
    such as profession, job position, job condition, and activity dates.
    """

    profession = SelectField(
        "Profesión",
        choices=[(e.name, e.value) for e in ProfessionsEnum],
        validators=[DataRequired(message="Debe seleccionar una profesión")],
        validate_choice=True,
    )
    position = SelectField(
        "Posición laboral",
        choices=[(e.name, e.value) for e in PositionEnum],
        validators=[DataRequired(message="Debe seleccionar una posición laboral")],
        validate_choice=True,
    )
    job_condition = SelectField(
        "Condición laboral",
        choices=[(e.name, e.value) for e in ConditionEnum],
        validators=[DataRequired(message="Debe seleccionar una condición laboral")],
        validate_choice=True,
    )
    start_date = DateField(
        "Inicio de actividades",
        validators=[DataRequired(message="Debe ingresar una fecha")],
        default=datetime.today,
    )
    end_date = DateField("Finalización de actividades", validators=[Optional()])
    is_active = BooleanField("Activo en la organización", default=True)


class EmployeeAddDocumentsForm(BaseManageDocumentsForm):
    """Form to tag documents when adding additional files for an employee.

    Fields:
        tag (SelectField): The tag to assign to the uploaded file.
    """
    tag = SelectField(
        "Etiqueta",
        choices=[(e.name, e.value) for e in FileTagEnum],
        validators=[
            DataRequired(
                message="Debe seleccionar lo que representa este archivo",
            )
        ],
        validate_choice=True,
    )


class EmployeeManagementForm(FlaskForm):
    """Form for creating a new employee, including validation of DNI and email.

    Fields:
        name (StringField): The employee's first name.
        lastname (StringField): The employee's last name.
        address (FormField): The employee's address.
        phone (FormField): The employee's phone number.
        employment_information (FormField): The employee's employment information.
        health_insurance (TextAreaField): The employee's health insurance.
        affiliate_number (StringField): The employee's health insurance affiliate number.
        emergency_contact (FormField): The employee's emergency contact information
    """

    def __init__(self, *args, **kwargs):
        super(EmployeeManagementForm, self).__init__(*args, **kwargs)
        self.current_email = None
        self.current_dni = None

    name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="Debe ingresar un nombre"),
            IsValidName()
        ]
    )
    lastname = StringField(
        "Apellido",
        validators=[
            DataRequired(message="Debe ingresar un apellido"),
            IsValidName()
        ]
    )
    address = FormField(AddressForm)
    phone = FormField(PhoneForm)
    employment_information = FormField(EmploymentInformationForm)
    health_insurance = TextAreaField("Obra Social", validators=[Optional()])
    affiliate_number = StringField("Numero de afiliado", validators=[Optional()])
    emergency_contact = FormField(EmergencyContactForm)


class EmployeeCreateForm(EmployeeManagementForm):
    """
    Form for creating a new employee record.

    Fields:
        dni (StringField): The employee's national ID (DNI).
        email (StringField): The employee's email address.
    """

    dni = StringField(
        "DNI",
        validators=[
            DataRequired(message="Debe ingresar un DNI"),
            Length(min=8, max=8, message="Debe ser un número de 8 digitos!"),
            IsValidDniNumber(),
            dni_existence,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Debe ingresar un email"),
            Email(message="Email inválido"),
            Length(max=100),
            email_existence,
        ],
    )


class EmployeeEditForm(EmployeeManagementForm):
    """
    Form for editing an existing employee record.

    Fields:
        id (HiddenField): The employee's unique ID.
        dni (StringField): The employee's national ID (DNI).
        email (StringField): The employee's email address.
    """

    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)
        self.current_email = kwargs.pop("current_email", None)
        self.current_dni = kwargs.pop("current_dni", None)

    id = HiddenField("ID")
    dni = StringField(
        "DNI",
        validators=[
            DataRequired(message="Debe ingresar un DNI"),
            Length(min=8, max=8, message="Debe ser un número de 8 digitos!"),
            IsNumber("Debe ser un numero de 8 digitos!"),
            dni_existence,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Debe ingresar un email"),
            Email(message="Email inválido"),
            Length(max=100, message="El email debe tener menos de 100 caracteres"),
            email_existence,
        ],
    )


class EmployeeSearchForm(BaseSearchForm):
    """
    Form for searching employee records based on multiple criteria.

    Fields:
        search_by (SelectField): Criteria to search by (e.g., name, DNI, email).
        order_by (SelectField): Criteria to order the search results.
        filter_is_active (SelectField): Filter by employee's active status.
        filter_job_position (SelectField): Filter by employee's job position.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_by.choices = [
            ("name", "Nombre"),
            ("lastname", "Apellido"),
            ("dni", "DNI"),
            ("email", "Email"),
        ]

        self.order_by.choices = [
            ("id", "ID"),
            ("name", "Nombre"),
            ("lastname", "Apellido"),
            ("dni", "DNI"),
            ("email", "Email"),
        ]

    filter_is_active = SelectField(
        choices=[
            ("", "Ver Todos"),
            ("true", "Activo"),
            ("false", "Inactivo"),
        ],
        validate_choice=True,
        validators=[Optional()],
    )
    filter_job_position = SelectField(
        "Puesto laboral",
        choices=[("", "Ver Todas")] + [(e.name, e.value) for e in PositionEnum],
        validate_choice=True,
    )


class EmployeeDocumentSearchForm(DocumentsSearchForm):
    """
    Form for searching employee documents based on document tags.

    Fields:
        filter_tag (SelectField): Filter by document tag (e.g., DNI, Title, Curriculum Vitae).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_tag.choices = [
            ("", "Ver Todos"),
        ] + [(e.name, e.value) for e in FileTagEnum]


class TrainerSearchForm(FlaskForm):
    """
    Form for searching for trainers by name or email.

    Fields:
        search_text (StringField): The text input for searching trainers.
        submit_search (SubmitField): The button to submit the search.
    """

    search_text = StringField(
        "Buscar por nombre o email",
        validators=[Length(message="El texto de búsqueda debe tener entre 1 y 50 caracteres", min=1, max=50)],
    )
    submit_search = SubmitField("Buscar")


class TrainerSelectForm(FlaskForm):
    """
    Form for selecting a trainer account.

    Fields:
        selected_trainer (HiddenField): The selected trainer's account ID.
        submit_trainer (SubmitField): The button to submit the trainer selection.
    """

    selected_trainer = HiddenField(
        "Cuenta seleccionada",
        validators=[DataRequired("Se debe seleccionar una cuenta"), IsNumber()],
    )
    submit_trainer = SubmitField("Asociar")

    def set_selected_account(self, account_id):
        """Sets the selected account for a trainer."""
        self.selected_trainer.data = account_id


class EmployeeSelectForm(FlaskForm):
    """
    Form for selecting an employee from a list.

    Fields:
        selected_item (HiddenField): The ID of the selected employee.
        submit_employee (SubmitField): The button to submit the employee selection.
    """

    selected_item = HiddenField(
        validators=[
            DataRequired("Se debe seleccionar un miembro del equipo"),
            IsNumber(),
        ],
    )
    submit_employee = SubmitField("Asociar")


class EmployeeMiniSearchForm(FlaskForm):
    """
    Form for performing a mini search for an employee by name or email.

    Fields:
        search_text (StringField): The text input for searching employees.
        submit_search (SubmitField): The button to submit the search.
    """

    search_text = StringField(
        "Miembro del equipo seleccionado",
        validators=[Length(message="El texto de búsqueda debe tener entre 0 y 50 caracteres", min=0, max=50)],
    )
    submit_search = SubmitField("Buscar")
