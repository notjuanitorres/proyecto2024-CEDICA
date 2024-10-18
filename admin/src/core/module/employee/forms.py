from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize, FileRequired
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from wtforms.fields import (
    StringField,
    BooleanField,
    SelectField,
    FormField,
    DateField,
    TextAreaField,
    SubmitField,
    FileField,
    MultipleFileField,
    HiddenField,
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
)


def email_existence(form, field):
    validator = EmailExistence(message="Email en uso")
    validator(form, field)


def dni_existence(form, field):
    validator = DniExistence(message="DNI en uso")
    validator(form, field)


class EmploymentInformationForm(FlaskForm):
    profession = SelectField(
        "Profesion",
        choices=[(e.name, e.value) for e in ProfessionsEnum],
        validators=[DataRequired()],
    )
    position = SelectField(
        "Posicion laboral",
        choices=[(e.name, e.value) for e in PositionEnum],
        validators=[DataRequired()],
    )
    job_condition = SelectField(
        "Condicion laboral",
        choices=[(e.name, e.value) for e in ConditionEnum],
        validators=[DataRequired()],
    )
    start_date = DateField(
        "Inicio de actividades",
        validators=[DataRequired()],
        default=datetime.today,
    )
    end_date = DateField("Finalizacion de actividades", validators=[Optional()])
    is_active = BooleanField("Activo en la organizacion", default=True)


def max_file_size(size_in_mb: int):
    BYTES_PER_MB = 1024 * 1024

    size_in_bytes = size_in_mb * BYTES_PER_MB

    return size_in_bytes


class EmployeeDocumentsForm(FlaskForm):
    dni = MultipleFileField(
        validators=[
            # FileRequired(),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                ["pdf", "jpg", "jpeg", "png"],
                message="Formato no reconocido. Formato valido: .pdf, .jpg, .jpeg, .png",
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
                ["pdf", "jpg", "jpeg", "png"],
                message="Formato no reconocido Formato valido: .pdf, .jpg, .jpeg, .png",
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
                upload_set=["pdf", "jpg", "jpeg", "png"],
                message="Formato no reconocido. Formato valido: .pdf",
            ),
        ]
    )


class EmployeeAddDocumentsForm(FlaskForm):
    tag = SelectField(
        "Tag",
        choices=[(e.name, e.value) for e in FileTagEnum],
        validators=[
            DataRequired(
                message="Debe seleccionar lo que representa este archivo",
            )
        ],
    )
    file = FileField(
        validators=[
            FileRequired("Debe adjuntar un archivo"),
            FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                upload_set=["pdf", "jpg", "jpeg", "png", "webp"],
                message="Formato no reconocido",
            ),
        ]
    )


class EmployeeManagementForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeManagementForm, self).__init__(*args, **kwargs)
        self.current_email = None
        self.current_dni = None

    name = StringField("Nombre", validators=[DataRequired()])
    lastname = StringField("Apellido", validators=[DataRequired()])
    address = FormField(AddressForm)
    phone = FormField(PhoneForm)
    employment_information = FormField(EmploymentInformationForm)
    health_insurance = TextAreaField("Obra Social", validators=[Optional()])
    affiliate_number = StringField("Numero de afiliado", validators=[Optional()])
    emergency_contact = FormField(EmergencyContactForm)
    documents = FormField(EmployeeDocumentsForm)

    # TODO: Find a way to relationate an account's email or id


class EmployeeCreateForm(EmployeeManagementForm):
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
    submit_another = SubmitField("Agregar otro")


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


class EmployeeSearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_by = SelectField(
        choices=[
            ("name", "Nombre"),
            ("lastname", "Apellido"),
            ("dni", "DNI"),
            ("email", "Email"),
        ],
        validate_choice=True,
    )
    search_text = StringField(validators=[Length(max=50)])
    filter_job_position = SelectField(
        "Puesto laboral",
        choices=[("", "Ver Todas")] + [(e.name, e.value) for e in PositionEnum],
        validate_choice=True,
    )
    filter_is_active = SelectField(
        choices=[
            ("", "Ver Todos"),
            ("true", "Activo"),
            ("false", "Inactivo"),
        ],
        validate_choice=True,
    )

    order_by = SelectField(
        choices=[
            ("id", "ID"),
            ("name", "Nombre"),
            ("lastname", "Apellido"),
            ("dni", "DNI"),
            ("email", "Email"),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[("asc", "Ascendente"), ("desc", "Descendente")], validate_choice=True
    )
    submit_search = SubmitField("Buscar")

class EmployeeAccountLinkForm(FlaskForm):
    positive_submit = SubmitField("Asociar")