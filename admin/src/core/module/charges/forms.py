from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DateField, DecimalField, HiddenField
from wtforms.validators import Length, DataRequired, Optional

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
    amount = DecimalField("Monto abonado", places=2, validators=[DataRequired()])
    date_of_charge = DateField("Fecha de pago", format='%Y-%m-%d', validators=[DataRequired()])
    payment_method = SelectField("Modo de pago",
                                 choices=[(p.name, p.value) for p in PaymentMethodEnum],
                                 validate_choice=True,
                                 validators=[DataRequired()],
                                 )

    observations = StringField("Observaciones", validators=[Length(max=255), DataRequired()])

    employee = StringField(
        "Empleado",
        validators=[DataRequired()],
        render_kw={"readonly": True}  # Hacer que el campo sea de solo lectura
    )
    employee_id = HiddenField(
        "ID del empleado",
        validators=[DataRequired()],
    )

    jya = StringField(
        "jya",
        validators=[Optional()],
        render_kw={"readonly": True}  # Hacer que el campo sea de solo lectura
    )
    jya_id = HiddenField(
        "jya_id",
        validators=[Optional()],
    )


class ChargeCreateForm(ChargeManagementForm):
    pass


class ChargeEditForm(ChargeManagementForm):
    def __init__(self, *args, **kwargs):
        super(ChargeEditForm, self).__init__(*args, **kwargs)
