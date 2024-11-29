from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DateField, DecimalField
from wtforms.validators import Length, DataRequired, Optional

from src.core.module.charges.models import PaymentMethodEnum

class ChargeSearchForm(FlaskForm):
    """
    Form for searching charges based on various criteria, including name, payment method, and date range.

    Fields:
        search_text (StringField): The text input for searching charges by jockey name.
        start_date (DateField): The start date for the search range.
        end_date (DateField): The end date for the search range.
        amount (DecimalField): The amount to filter charges.
        payment_method (SelectField): Filter by payment method.
        limit (SelectField): The number of results to display per page.
        submit_search (SubmitField): The button to submit the search.
    """

    search_text = StringField(
        "Buscar por nombre",
        validators=[
            Length(max=50, message="El texto de búsqueda no puede superar los 50 caracteres."),
            Optional()
        ]
    )

    start_date = DateField("Fecha de Inicio", format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField("Fecha de Fin", format='%Y-%m-%d', validators=[Optional()])

    amount = DecimalField("Monto", places=2, validators=[Optional()])

    payment_method = SelectField(
        "Método de Pago",
        choices=[("", "Todos")] + [(p.name, p.value) for p in PaymentMethodEnum],
        validate_choice=True,
        validators=[Optional()]
    )

    limit = SelectField(
        "Cantidad a mostrar",
        choices=[("10", "10"), ("25", "25"), ("50", "50"), ("100", "100")],
        validate_choice=True,
        validators=[Optional()]
    )

    submit_search = SubmitField("Filtrar")

    def __init__(self, *args, **kwargs):
        """
        Constructor for the ChargeSearchForm class.

        Args:
            *args: Arbitrary arguments.
            **kwargs: Arbitrary keyword arguments.
        """
        cantidad = kwargs.pop('max', None)
        super(ChargeSearchForm, self).__init__(*args, **kwargs)
        if cantidad:
            self.limit.choices = [(str(i * 10), str(i * 10)) for i in range(1, (cantidad // 10) + 1)]
            self.limit.choices.append((str(cantidad), str(cantidad)))

    def validate(self, **kwargs):
        """
        Custom validation function to ensure valid date range selection.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        if isinstance(self.start_date.errors, tuple):
            self.start_date.errors = list(self.start_date.errors)
        if isinstance(self.end_date.errors, tuple):
            self.end_date.errors = list(self.end_date.errors)

        if self.start_date.data and not self.end_date.data:
            self.end_date.errors.append('Se deben seleccionar ambas fechas.')
            return False
        if not self.start_date.data and self.end_date.data:
            self.start_date.errors.append('Se deben seleccionar ambas fechas.')
            return False

        if self.start_date.data and self.end_date.data and self.start_date.data > self.end_date.data:
            self.start_date.errors.append('La fecha de inicio no puede ser mayor a la fecha de fin.')
            return False

        return True