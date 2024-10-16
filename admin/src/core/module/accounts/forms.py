from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from .validators import EmailExistence

from src.core.module.accounts.models import RoleEnum
from src.core.module.common.forms import BaseSearchForm


def email_existence(form, field):
    validator = EmailExistence(message="Email en uso")
    validator(form, field)


class UserManagementForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(UserManagementForm, self).__init__(*args, **kwargs)

        self.role_id.choices = self.get_role_choices()

    def get_role_choices(self):
        return [(role.id, role.name) for role in self.import_validator().get_roles()]

    def import_validator(self):
        # Needed to import the container dynamically at run time
        # It is in order to work along with WTForms instantiation at definition
        # pylint: disable="C0415"
        from src.core.container import Container

        container = Container()
        return container.accounts_services()

    role_id = SelectField(
        "Rol",
        coerce=int,
        validators=[Optional()],
    )

    email = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email(message="Email inválido"),
            email_existence,
            Length(max=100)
        ],
    )
    alias = StringField("Alias", validators=[DataRequired(), Length(min=3, max=15)])

    enabled = BooleanField("Habilitado", default=True)

    system_admin = BooleanField("System Admin", default=False)


class UserCreateForm(UserManagementForm):
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

    current_email = None


class UserEditForm(UserManagementForm):

    def __init__(self, *args, **kwargs):
        self.current_email = kwargs.pop('current_email', None)
        super(UserEditForm, self).__init__(*args, **kwargs)


class UserLoginForm(FlaskForm):
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


class UserSearchForm(BaseSearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_by.choices = [
            ("email", "Email"),
        ]
        self.order_by.choices = [
            ("id", "ID"),
            ("email", "Email"),
        ]

    filter_enabled = SelectField(
        choices=[
            ("true", "Si"),
            ("false", "No"),
            ("", "Todos"),
        ],
        validate_choice=True,
    )

    filter_role_id = SelectField(
        choices=[('', 'Todos')] +
                [(str(index + 1), role.value) for index, role in enumerate(RoleEnum)],
    )
