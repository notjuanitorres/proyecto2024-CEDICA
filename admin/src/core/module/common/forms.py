from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields import (
    IntegerField,
    StringField,
    TelField,
)
from .validators import IsNumber


class AddressForm(FlaskForm):
    street = StringField("Calle", validators=[DataRequired(), Length(max=50)])
    number = IntegerField("Numero", validators=[DataRequired()])
    department = StringField("Departamento", validators=[Optional(), Length(max=50)])
    locality = StringField("Localidad", validators=[DataRequired(), Length(max=50)])
    province = StringField("Provincia", validators=[DataRequired(), Length(max=50)])


class PhoneForm(FlaskForm):
    country_code = TelField(
        "Codigo de pais", validators=[DataRequired(), Length(max=5)]
    )
    area_code = TelField(
        "Codigo de area", validators=[DataRequired(), Length(max=5), IsNumber()]
    )
    number = TelField(
        "Numero", validators=[DataRequired(), Length(min=9, max=15), IsNumber()]
    )


class EmergencyContactForm(FlaskForm):
    emergency_contact_name = StringField(
        "Nombre contacto de emergencia", validators=[DataRequired(), Length(max=50)]
    )
    emergency_contact_phone = TelField(
        "Telefono contacto de emergencia", validators=[DataRequired()]
    )
