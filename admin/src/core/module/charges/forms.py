from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DateField, DecimalField
from wtforms.validators import Length, DataRequired

from src.core.module.charges.models import PaymentMethodEnum


class ChargeSearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_by = SelectField(
        choices=[
            ("name", "Nombre"),
            ("lastname", "Apellido"),
        ],
        validate_choice=True,
    )
    search_text = StringField(validators=[Length(max=50)])

    filter_payment_method = (
        SelectField("Método de pago",
                    choices=[("", "Ver Todas")] + [(p.name, p.value) for p in PaymentMethodEnum],
                    validate_choice=True,
                    ))

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

    # Custom validation function (redefine built-in)
    def validate(self, **kwargs):
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
    # jya_id = # TODO: use component from payments search form
    amount = DecimalField(places=2, validators=[DataRequired()])
    date_of_charge = DateField("Fecha de pago", format='%Y-%m-%d')
    payment_method = SelectField(
        choices=[(p.name, p.value) for p in PaymentMethodEnum],
        validate_choice=True,
    )
    # employee_id = # TODO: use component from payments search form
    observations = StringField(validators=[Length(max=255)])


class ChargeCreateForm(ChargeManagementForm):
    pass


class ChargeEditForm(ChargeManagementForm):
    def __init__(self, *args, **kwargs):
        super(ChargeEditForm, self).__init__(*args, **kwargs)
