from datetime import datetime
from src.core.module.payment.data import PaymentTypeEnum as types
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, DecimalField, HiddenField
from wtforms.validators import DataRequired, Length, Optional


class PaymentForm(FlaskForm):
    """
    Form for creating and editing payments.

    Attributes:
        amount (DecimalField): The amount to be paid.
        date (DateField): The date of the payment.
        description (StringField): The description of the payment.
        payment_type (SelectField): The type of payment.
        beneficiary (StringField): The beneficiary of the payment (read-only).
        beneficiary_id (HiddenField): The ID of the beneficiary.
        submit (SubmitField): The submit button for the form.
    """
    def __init__(self, *args, **kwargs):
        """Initialize the PaymentForm."""
        super(PaymentForm, self).__init__(*args, **kwargs)

    amount = DecimalField(
        "Monto a pagar",
        validators=[
            DataRequired(message="Debe ingresar un monto"),
        ],
        places=2,
    )
    date = DateField(
        "Fecha del pago",
        validators=[
            DataRequired(message="Debe ingresar una fecha"),
        ],
        default=datetime.today,
    )
    description = StringField(
        "Descripción",
        validators=[
            DataRequired(message="Debe ingresar una descripción"),
            Length(max=100, message="La descripción no puede tener más de 100 caracteres"),
        ],
    )
    payment_type = SelectField(
        "Tipo de pago",
        choices=[(e.name, e.value) for e in types],
        validators=[DataRequired(message="Debe seleccionar un tipo de pago")],
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
    """
    Form for searching payments.

    Attributes:
        start_date (DateField): The start date for the search.
        end_date (DateField): The end date for the search.
        payment_type (SelectField): The type of payment to search for.
        order_by (SelectField): The field to order the results by.
        order (SelectField): The order direction (ascending or descending).
        submit_search (SubmitField): The submit button for the search form.
    """
    def __init__(self, *args, **kwargs):
        """Initialize the PaymentSearchForm with choices for order_by and order fields."""
        super(PaymentSearchForm, self).__init__(*args, **kwargs)
        self.order_by.choices = [('payment_date', 'Fecha de Pago'), ('payment_type', 'Tipo de Pago')]
        self.order.choices = [('asc', 'Ascendente'), ('desc', 'Descendente')]

    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('Fecha de fin', format='%Y-%m-%d', validators=[Optional()])
    payment_type = SelectField(
        'Tipo de pago',
        choices=[('', 'Todos'), ('HONORARIOS', 'Honorarios'), ('PROOVEDOR', 'Proveedor'), ('GASTOS', 'Gastos Varios')],
        validators=[Optional()],
        validate_choice=True
    )
    order_by = SelectField(
        'Ordenar por',
        choices=[('payment_date', 'Fecha de Pago'), ('amount', 'Monto')],
        validators=[Optional()],
        validate_choice=True
    )
    order = SelectField(
        'En orden',
        choices=[('asc', 'Ascendente'), ('desc', 'Descendente')],
        validators=[Optional()],
        validate_choice=True
    )
    submit_search = SubmitField("Buscar")

    
class PaymentEditForm(PaymentForm):
    """Class for editing payments."""
    def __init__(self, *args, **kwargs):
        """Initialize the PaymentEditForm."""
        super(PaymentEditForm, self).__init__(*args, **kwargs)