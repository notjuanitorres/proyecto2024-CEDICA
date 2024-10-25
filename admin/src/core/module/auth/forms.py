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
            DataRequired(message="El email es obligatorio"),
            Email(message="Email inválido"),
            Length(max=100, message="El email debe tener menos de 100 caracteres"),],
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(
                min=8, max=255, message="La contraseña debe tener más de 8 caracteres y menos de 255"
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
            DataRequired("El email es obligatorio"),
            Email(message="Email inválido"),
            email_existence,
            Length(max=100, message="El email debe tener menos de 100 caracteres"),
        ],
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(
                min=8, max=255, message="La contraseña debe tener más de 8 caracteres y menos de 255"
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="La confirmación de la contraseña es obligatoria"),
            EqualTo("password", message="Las contraseñas deben coincidir"),
        ],
    )

    alias = StringField(
        "Alias",
        validators=[
            DataRequired(message="El alias es obligatorio"),
            Length(min=3, max=15, message="El alias debe tener entre 3 y 15 caracteres"),
        ]
    )
