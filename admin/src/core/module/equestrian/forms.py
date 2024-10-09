from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, SelectMultipleField, widgets, SubmitField
from wtforms.validators import DataRequired, Length
from src.core.module.equestrian.models import JAEnum


class MultiCheckboxField(SelectMultipleField):
    """
    https://wtforms.readthedocs.io/en/3.0.x/specific_problems/?highlight=listwidget#specialty-field-tricks
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class HorseManagementForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
    )

    breed = StringField(
        "Raza",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
    )

    birth_date = DateField(
        "Fecha de nacimiento",
        validators=[
            DataRequired(),
        ],
    )

    sex = SelectField(
        "Sexo",
        choices=[('M', 'Macho'), ('H', 'Hembra')],
        validators=[
            DataRequired(),
        ],
    )

    coat = StringField(
        "Pelaje",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
    )

    is_donation = BooleanField("Es donación", default=False)

    admission_date = DateField(
        "Fecha de ingreso",
        validators=[
            DataRequired(),
        ],
    )

    assigned_facility = StringField(
        "Facilidad asignada",
        validators=[
            DataRequired(),
            Length(max=100),
        ],
    )

    ja_type = SelectField(
        "Tipo de J&A asignado",
        choices=[
            (JAEnum.HIPOTHERAPY.name, JAEnum.HIPOTHERAPY.value),
            (JAEnum.THERAPEUTIC_RIDING.name, JAEnum.THERAPEUTIC_RIDING.value),
            (JAEnum.ADAPTED_SPORTS.name, JAEnum.ADAPTED_SPORTS.value),
            (JAEnum.RECREATIONAL_ACTIVITIES.name, JAEnum.RECREATIONAL_ACTIVITIES.value),
            (JAEnum.RIDING.name, JAEnum.RIDING.value),
        ],
        validators=[
            DataRequired(),
        ],
    )


class HorseCreateForm(HorseManagementForm):
    pass


class HorseEditForm(HorseManagementForm):
    def __init__(self, *args, **kwargs):
        super(HorseEditForm, self).__init__(*args, **kwargs)
        self.trainers.choices = self.get_trainers_choices()

    def import_validator(self):
        # Needed to import the container dynamically at run time
        # It is in order to work along with WTForms instantiation at definition
        # pylint: disable="C0415"
        from src.core.container import Container

        container = Container()
        return container.employee_services()

    def get_trainers_choices(self):
        return [(trainer.id, trainer.name) for trainer in self.import_validator().get_trainers()]

    trainers = MultiCheckboxField(
        "Entrenadores y conductores",
        choices=[],
        # TODO: get the horse trainers and set them as checked
    )


class HorseSearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_by = SelectField(
        choices=[
            ("name", "Nombre"),
        ],
        validate_choice=True,
    )
    search_text = StringField(validators=[Length(max=50)])

    filter_ja_type = SelectField(
        choices=[("", "Ver Todos")] + [(jtype.name, jtype.value) for jtype in JAEnum],
        validate_choice=True,
    )
    order_by = SelectField(
        choices=[
            ("id", "ID"),
            ("name", "Nombre"),
            ("birth_date", "Fecha de nacimiento"),
            ("admission_date", "Fecha de ingreso"),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[("asc", "Ascendente"), ("desc", "Descendente")], validate_choice=True
    )
    submit_search = SubmitField("Buscar")
