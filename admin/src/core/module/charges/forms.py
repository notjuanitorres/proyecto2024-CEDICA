from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DateField, DecimalField, HiddenField
from wtforms.validators import Length, DataRequired, Optional

from src.core.module.charges.models import PaymentMethodEnum


class ChargeSearchForm(FlaskForm):
    """
    Form for searching charges based on various criteria, including name, payment method, and date range.

    Fields:
        search_by (SelectField): Criteria to search by (e.g., name, lastname).
        search_text (StringField): The text input for searching charges.
        filter_payment_method (SelectField): Filter by payment method.
        start_date (DateField): The start date for the search range.
        finish_date (DateField): The end date for the search range.
        order_by (SelectField): Criteria to order the search results.
        order (SelectField): Order direction (ascendente or descendente).
        submit_search (SubmitField): The button to submit the search.
    """

    class Meta:
        """Metaclass to disable CSRF protection."""
        csrf = False

    search_by = SelectField(
        choices=[
            ("name", "Nombre"),
            ("lastname", "Apellido"),
        ],
        validate_choice=True,
    )
    search_text = StringField(validators=[Length(max=50)])

    filter_payment_method = SelectField(
        "Método de pago",
        choices=[("", "Ver Todas")] + [(p.name, p.value) for p in PaymentMethodEnum],
        validate_choice=True,
    )

    start_date = DateField("Fecha de inicio", format='%Y-%m-%d')
    finish_date = DateField("Fecha de fin", format='%Y-%m-%d')

    order_by = SelectField(
        choices=[
            ("id", "ID"),
            ("date_of_charge", "Fecha de pago"),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[("asc", "Ascendente"), ("desc", "Descendente")], validate_choice=True
    )
    submit_search = SubmitField("Buscar")

    def validate(self, **kwargs):
        """
        Custom validation function to ensure valid date range selection.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        # Don't validate if no search is submitted
        if not self.start_date.data and not self.finish_date.data:
            return True

        # Ensure that if one date is selected the other is too
        if self.start_date.data and not self.finish_date.data:
            self.finish_date.errors = []
            self.finish_date.errors.append('Se deben seleccionar ambas fechas.')
            return False
        if not self.start_date.data and self.finish_date.data:
            self.start_date.errors = []
            self.start_date.errors.append('Se deben seleccionar ambas fechas.')
            return False

        # Ensure end date >= start date
        if self.start_date.data > self.finish_date.data:
            self.start_date.errors = []
            self.start_date.errors.append('La fecha de inicio no puede ser mayor a la fecha de fin.')
            return False

        return True


class ChargeManagementForm(FlaskForm):
    """
    Form for managing charge information, including amount, date of charge, payment method, and observations.

    Fields:
        amount (DecimalField): The amount of the charge.
        date_of_charge (DateField): The date of the charge.
        payment_method (SelectField): The payment method used for the charge.
        observations (StringField): Additional observations about the charge.
    """

    amount = DecimalField("Monto abonado", places=2, validators=[DataRequired()])
    date_of_charge = DateField("Fecha de pago", format='%Y-%m-%d', validators=[DataRequired()])
    payment_method = SelectField(
        "Modo de pago",
        choices=[(p.name, p.value) for p in PaymentMethodEnum],
        validate_choice=True,
        validators=[DataRequired()],
    )
    observations = StringField("Observaciones", validators=[Length(max=255), DataRequired()])


class ChargeCreateForm(ChargeManagementForm):
    """
    Form for creating a new charge.

    Inherits all fields from ChargeManagementForm.
    """
    pass


class ChargeEditForm(ChargeManagementForm):
    """
    Form for editing an existing charge.

    Inherits all fields from ChargeManagementForm.
    """
    pass