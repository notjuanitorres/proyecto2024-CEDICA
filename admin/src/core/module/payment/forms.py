from datetime import datetime
from random import choices
from src.core.module.payment.data import payment_type as types
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, DecimalField
from wtforms.validators import DataRequired, Length

class PaymentForm(FlaskForm):

    amount = DecimalField(
        "Monto a pagar",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
        places=2,
    )
    date= DateField(
        "Fecha del pago",
        validators=[
            DataRequired(),
        ],
        default=datetime.today,
    )
    description = StringField(
        "Descripción",
        validators=[
            DataRequired(),
            Length(max=100)
        ],
    )
    payment_type = SelectField(
        "Tipo de pago",
        choices=[(e.name, e.value) for e in types],
        validators=[DataRequired()],
    )
    beneficiary = StringField( # IMPLEMENTAR MODAL PARA SELECCIONAR BENEFICIARIO
        "Beneficiario",
        validators=[
            DataRequired(),
            Length(max=100)
        ],
    )

    submit = SubmitField("Submit")