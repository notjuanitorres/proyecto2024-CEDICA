"""
forms.py

This module defines forms for the messages between public portal and the administration
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


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
