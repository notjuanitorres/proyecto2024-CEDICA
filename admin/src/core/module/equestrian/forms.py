from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length
from src.core.module.equestrian.models import JAEnum


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
    pass
