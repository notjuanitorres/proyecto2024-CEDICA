from datetime import datetime
from random import choices
from src.core.module.payment.data import PaymentType
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length

class PaymentForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

    amount = StringField(
        "Amount",
        validators=[
            DataRequired(),
            Length(max=100)
        ],
    )
    date= DateField(
        "Date",
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
        choichoices=[(e.name, e.value) for e in PaymentType],
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