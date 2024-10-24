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
    validator = EmailExistence(message="Email en uso")
    validator(form, field)


def dni_existence(form, field):
    validator = DniExistence(message="DNI en uso")
    validator = DniExistence(message="DNI en uso")
    validator(form, field)


class EmploymentInformationForm(FlaskForm):
    profession = SelectField(
        "Profesión",
        choices=[(e.name, e.value) for e in ProfessionsEnum],
        validators=[DataRequired()],
        validate_choice=True,
    )
    position = SelectField(
        "Posición laboral",
        choices=[(e.name, e.value) for e in PositionEnum],
        validators=[DataRequired()],
        validate_choice=True,
    )
    job_condition = SelectField(
        "Condición laboral",
        choices=[(e.name, e.value) for e in ConditionEnum],
        validators=[DataRequired()],
        validate_choice=True,
    )
    start_date = DateField(
        "Inicio de actividades",
        validators=[DataRequired()],
        default=datetime.today,
    )
    end_date = DateField("Finalización de actividades", validators=[Optional()])
    is_active = BooleanField("Activo en la organización", default=True)


class EmployeeDocumentsForm(FlaskForm):
    dni = MultipleFileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                allowed_filetypes,
                message=filetypes_message,
            ),
            FilesNumber(min=0, max=2, message="Puede subir hasta 2 archivos"),
        ]
    )
    title = MultipleFileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                allowed_filetypes,
                message=filetypes_message,
            ),
            FilesNumber(min=0, max=5, message="Puede subir hasta 5 archivos"),
        ]
    )
    curriculum_vitae = FileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                upload_set=allowed_filetypes,
                message=filetypes_message,
            ),
        ]
    )


class EmployeeAddDocumentsForm(BaseManageDocumentsForm):
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


class EmployeeManagementForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeManagementForm, self).__init__(*args, **kwargs)
        self.current_email = None
        self.current_dni = None

    name = StringField("Nombre", validators=[DataRequired(), IsValidName()])
    lastname = StringField("Apellido", validators=[DataRequired(), IsValidName()])
    address = FormField(AddressForm)
    phone = FormField(PhoneForm)
    employment_information = FormField(EmploymentInformationForm)
    health_insurance = TextAreaField("Obra Social", validators=[Optional()])
    affiliate_number = StringField("Numero de afiliado", validators=[Optional()])
    emergency_contact = FormField(EmergencyContactForm)

    # TODO: Find a way to relationate an account's email or id


class EmployeeCreateForm(EmployeeManagementForm):
    dni = StringField(
        "DNI",
        validators=[
            DataRequired(),
            Length(min=8, max=8),
            IsNumber("Debe ser un número de 8 digitos!"),
            dni_existence,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email inválido"),
            Length(max=100),
            email_existence,
        ],
    )


class EmployeeEditForm(EmployeeManagementForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)
        self.current_email = kwargs.pop("current_email", None)
        self.current_dni = kwargs.pop("current_dni", None)

    id = HiddenField("ID")
    dni = StringField(
        "DNI",
        validators=[
            DataRequired(),
            Length(min=8, max=8),
            IsNumber("Debe ser un numero de 8 digitos!"),
            dni_existence,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email inválido"),
            Length(max=100),
            email_existence,
        ],
    )


class EmployeeSearchForm(BaseSearchForm):
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
        validators=[Optional()]
    )
    filter_job_position = SelectField(
        "Puesto laboral",
        choices=[("", "Ver Todas")] + [(e.name, e.value) for e in PositionEnum],
        validate_choice=True,
    )


class EmployeeDocumentSearchForm(DocumentsSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_tag.choices = [
            ("", "Ver Todos"),
        ] + [(e.name, e.value) for e in FileTagEnum]


class TrainerSearchForm(FlaskForm):
    search_text = StringField(
        "Buscar por nombre o email", validators=[Length(message="Debe ingresar un texto", min=1, max=50)]
    )
    submit_search = SubmitField("Buscar")


class TrainerSelectForm(FlaskForm):
    selected_trainer = HiddenField(
        "Cuenta seleccionada",
        validators=[DataRequired("Se debe seleccionar una cuenta"), IsNumber()],
    )
    submit_trainer = SubmitField("Asociar")

    def set_selected_account(self, account_id):
        self.selected_trainer.data = account_id

class EmployeeSelectForm(FlaskForm):
    selected_item = HiddenField(
        validators=[DataRequired("Se debe seleccionar un miembro del equipo"), IsNumber()],
    )
    submit_employee = SubmitField("Asociar")


class EmployeeMiniSearchForm(FlaskForm):
    search_text = StringField(
        "Miembro del equipo seleccionado",
        validators=[Length(message="Debe ingresar un texto", min=1, max=50)])
    submit_search = SubmitField("Buscar")
