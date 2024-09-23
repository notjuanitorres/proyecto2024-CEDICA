from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from .validators import EmailExistence

class UserCreateForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email invalido"),
            EmailExistence("El email se encuentra en uso"),
            Length(max=100),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=8, max=255, message="La contrasena debe tener mas de 8 caracteres"
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contrasenas deben coincidir"),
        ],
    )

    role_id = SelectField(
        "Role",
        coerce=int,
        # TODO: Choices should be a list of the roles stored on the DB and retrieved from there
        choices=[
            (1, "Admin"),
            (2, "Voluntario"),
            (3, "Equestre"),
            (4, "Tecnico"),
        ],
        validators=[Optional()],
    )
    alias = StringField("Alias", validators=[
        DataRequired(), Length(min=3, max=15)])

    enabled = BooleanField("Enabled", default=True)

    system_admin = BooleanField("System Admin", default=False)


def email_existence(form, field):
    validator = EmailExistence("Email en uso")
    validator(form, field)

class UserEditForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        self.current_email = kwargs.pop('current_email', None)
        super(UserEditForm, self).__init__(*args, **kwargs)


    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Email invalido"),
            email_existence,
            Length(max=100)
        ],
    )
    role_id = SelectField(
        "Role",
        coerce=int,
        # TODO: Choices should be a list of the roles stored on the DB and retrieved from there
        choices=[
            (1, "Admin"),
            (2, "Voluntario"),
            (3, "Equestre"),
            (4, "Tecnico"),
        ],
        validators=[Optional()],
    )

    alias = StringField("Alias", validators=[DataRequired(), Length(min=3, max=15)])

    enabled = BooleanField("Enabled", default=True)

    system_admin = BooleanField("System Admin", default=False)


class UserLoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(
            message="Email invalido"), Length(max=100)],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=8, max=255, message="La contrasena debe tener mas de 8 caracteres"
            ),
        ],
    )
