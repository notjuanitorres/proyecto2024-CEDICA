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
)
from src.core.module.employee.data import ProfessionsEnum, PositionEnum, ConditionEnum
from src.core.module.common import AddressForm, EmergencyContactForm, PhoneForm


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
    dni = StringField("DNI", validators=[DataRequired(), Length(min=8, max=8)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Email inválido"), Length(max=100)],
    )


class EmployeeEditForm(EmployeeManagementForm):
    dni = StringField("DNI", validators=[DataRequired(), Length(min=8, max=8)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Email inválido"), Length(max=100)],
    )
