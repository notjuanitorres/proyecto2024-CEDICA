from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class UserCreateForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Email invalido"), Length(max=100)],
    )

    alias = StringField("Alias", validators=[DataRequired(), Length(min=3, max=15)])

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

    enabled = BooleanField("Enabled", default=True)

    system_admin = BooleanField("System Admin", default=False)

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


class UserLoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Email invalido"), Length(max=100)],
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
