from datetime import datetime
from random import choices
from src.core.module.payment.data import payment_type as types
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, DecimalField, HiddenField
from wtforms.validators import DataRequired, Length, Optional

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
    beneficiary = StringField(
        "Beneficiario",
        validators=[Optional()],
        render_kw={"readonly": True}  # Hacer que el campo sea de solo lectura
    )
    beneficiary_id = HiddenField(
        "Beneficiary ID",
        validators=[Optional()],
    )

    submit = SubmitField("Submit")
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if self.payment_type.data == 'HONORARIOS' and not self.beneficiary_id.data:
            self.beneficiary.errors.append('El beneficiario es obligatorio para pagos de honorarios.')
            return False

        return True