"""
forms.py

This module defines forms for the messages between public portal and the administration
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from .models import MessageStateEnum

class ContactMessageForm(FlaskForm):
    """
    Base form for submitting a contact message
    """

    email = StringField(
        "Correo",
        validators=[
            DataRequired(message="Debe ingresar un correo"),
            Email(message="Email inválido"),
            Length(max=100, message="El correo debe tener menos de 100 caracteres"),
        ],
    )
    name = StringField(
        "Nombre Completo",
        validators=[
            DataRequired(message="Debe ingresar su nombre completo"),
            Length(max=50, message="El nombre debe tener menos de 50 caracteres"),
        ],
    )
    message = StringField(
        "Mensaje",
        validators=[
            DataRequired(message="Debe escribir un mensaje"),
            Length(max=5000, message="El correo debe tener menos de 5000 caracteres"),
        ],
    )

class ContactSearchForm(FlaskForm):
    search_by = SelectField(
        choices=[
            ("email", "Email"),
            ("name", "Nombre"),
        ],
        validate_choice=True,
    )
    search_text = StringField(
        validators=[
            Length(max=50, message="El texto de búsqueda no puede superar los 50 caracteres.")
        ]
    )

    filter_status = SelectField(
        "Estado",
        choices=[("", "Ver Todas")] + [(s.name, s.value) for s in MessageStateEnum],
        validate_choice=True,
    )

    start_date = DateField("Fecha de inicio", format='%Y-%m-%d')
    end_date = DateField("Fecha de fin", format='%Y-%m-%d')

    order_by = SelectField(
        choices=[
            ("id", "ID"),
            ("title", "Título"),
            ("create_date", "Fecha de recepcion"),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[("asc", "Ascendente"), ("desc", "Descendente")],
        validate_choice=True
    )
    submit_search = SubmitField("Buscar")
