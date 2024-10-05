from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields import (
    IntegerField,
    StringField,
    FormField,
    TelField,
)


class AddressForm(FlaskForm):
    street = StringField("Calle", validators=[DataRequired(), Length(max=50)])
    number = IntegerField("Numero", validators=[DataRequired()])
    department = StringField("Departamento", validators=[Optional(), Length(max=50)])
    locality = StringField("Localidad", validators=[DataRequired(), Length(max=50)])
    province = StringField("Provincia", validators=[DataRequired(), Length(max=50)])


class TelephoneForm(FlaskForm):
    country_code = TelField("Codigo de pais", validators=[DataRequired(), Length(max=5)])
    area_code = TelField("Codigo de area", validators=[DataRequired(), Length(max=5)])
    number = TelField("Numero", validators=[DataRequired(), Length(max=15)])


class BasicInformationForm(FlaskForm):
    first_name = StringField("Nombre", validators=[DataRequired()])
    last_name = StringField("Apellido", validators=[DataRequired()])
    phone = FormField(TelephoneForm)
    dni = StringField("DNI", validators=[DataRequired(), Length(min=8, max=8)])


class EmergencyContactForm(FlaskForm):
    emergency_contact_name = StringField(
        "Nombre contacto de emergencia", validators=[DataRequired(), Length(max=50)]
    )
    emergency_contact_phone = TelField(
        "Telefono contacto de emergencia", validators=[DataRequired()]
    )
