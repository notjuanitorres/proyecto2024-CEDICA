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
from src.core.module.common import (
    AddressForm,
    EmergencyContactForm,
    BasicInformationForm,
)


class EmployeeManagementForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeManagementForm, self).__init__(*args, **kwargs)


class EmployeeCreateForm(EmployeeManagementForm):
    basic_information = FormField(BasicInformationForm)
    address = FormField(AddressForm)
    emergency_contact = FormField(EmergencyContactForm)
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Email inválido"), Length(max=100)],
    )
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
    end_date = DateField(
        "Finalizacion de actividades", validators=[Optional()]
    )
    health_insurance = TextAreaField("Obra Social", validators=[Optional()])
    affiliate_number = StringField("Numero de afiliado", validators=[Optional()])
    is_active = BooleanField(
        "Activo en la organizacion", default=True, validators=[DataRequired()]
    )
    # user_id = IntegerField("", validators=[DataRequired()])


class EmployeeEditForm(EmployeeManagementForm):
    pass
