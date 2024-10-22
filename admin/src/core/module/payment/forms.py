from datetime import datetime
from random import choices
from src.core.module.payment.data import PaymentTypeEnum as types
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, DecimalField, HiddenField
from wtforms.validators import DataRequired, Length, Optional

class PaymentForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
    amount = DecimalField(
        "Monto a pagar",
        validators=[
            DataRequired(),
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
        validate_choice=True
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

    
class PaymentSearchForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(PaymentSearchForm, self).__init__(*args, **kwargs)
        self.order_by.choices = [('payment_date', 'Fecha de Pago'), ('payment_type', 'Tipo de Pago')]
        self.order.choices = [('asc', 'Ascendente'), ('desc', 'Descendente')]

    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    payment_type = SelectField('Payment Type', choices=[
        ('', 'Todos'),
        ('HONORARIOS', 'Honorarios'),
        ('PROOVEDOR', 'Proveedor'),
        ('GASTOS', 'Gastos Varios')
    ], validators=[Optional()])
    order_by = SelectField('Order By', choices=[('payment_date', 'Fecha de Pago'), ('amount', 'Monto')], validators=[Optional()])
    order = SelectField('Order', choices=[('asc', 'Ascendente'), ('desc', 'Descendente')], validators=[Optional()])
    submit_search = SubmitField("Buscar")

    
class PaymentEditForm(PaymentForm):

    def __init__(self, *args, **kwargs):
        super(PaymentEditForm, self).__init__(*args, **kwargs)