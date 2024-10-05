from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.fields import (
    StringField,
    BooleanField,
    SelectField,
    FormField,
    DateField,
    TextAreaField,
    SubmitField,
)
from src.core.module.employee.data import ProfessionsEnum, PositionEnum, ConditionEnum
from src.core.module.employee.validators import EmailExistence, DniExistence
from src.core.module.common import AddressForm, EmergencyContactForm, PhoneForm


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
    is_active = BooleanField("Activo en la organizacion")


class EmployeeManagementForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeManagementForm, self).__init__(*args, **kwargs)
        self.current_email = None
        self.current_dni = None

    first_name = StringField("Nombre", validators=[DataRequired()])
    last_name = StringField("Apellido", validators=[DataRequired()])
    address = FormField(AddressForm)
    phone = FormField(PhoneForm)
    employment_information = FormField(EmploymentInformationForm)
    health_insurance = TextAreaField("Obra Social", validators=[Optional()])
    affiliate_number = StringField("Numero de afiliado", validators=[Optional()])
    emergency_contact = FormField(EmergencyContactForm)

    # user_id = IntegerField("", validators=[DataRequired()])


class EmployeeCreateForm(EmployeeManagementForm):
    dni = StringField(
        "DNI", validators=[DataRequired(), Length(min=8, max=8), dni_existence]
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

    dni = StringField(
        "DNI", validators=[DataRequired(), Length(min=8, max=8), dni_existence]
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
    filter_profession = SelectField(
        choices=[("", "Ver Todas")] + [(e.name, e.value) for e in ProfessionsEnum],
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
