from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from src.core.module.user.validators import EmailExistence


def email_existence(form, field):
    """
    Check if the email is assigned to another user.

    Args:
        form: The form object that includes the field.
        field: The field object representing the email input.
    """
    validator = EmailExistence(message="Email en uso")
    validator(form, field)


class UserLoginForm(FlaskForm):
    """
    Form for user login.

    Fields:
        email (StringField): The email address of the user.
        password (PasswordField): The password of the user.
    """

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email inválido"),
            Length(max=100)],
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(
                min=8, max=255, message="La contraseña debe tener más de 8 caracteres"
            ),
        ],
    )


class UserRegisterForm(FlaskForm):
    """
    Form for user registration.

    Fields:
        email (StringField): The email address of the user.
        password (PasswordField): The password of the user.
        confirm_password (PasswordField): The confirmation of the password.
        alias (StringField): The alias or username of the user.
    """

    current_email = None

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email inválido"),
            email_existence,
            Length(max=100),
        ],
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(
                min=8, max=255, message="La contraseña debe tener más de 8 caracteres"
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas deben coincidir"),
        ],
    )

    alias = StringField(
        "Alias",
        validators=[
            DataRequired(),
            Length(min=3, max=15)
        ]
    )