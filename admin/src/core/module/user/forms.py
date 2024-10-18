from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SelectField,
    SubmitField,
    HiddenField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from src.core.module.common.validators import IsNumber
from src.core.module.auth.data import RoleEnum
from .validators import EmailExistence


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
        return container.auth_services()

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
            Length(max=100),
        ],
    )
    alias = StringField("Alias", validators=[DataRequired(), Length(min=3, max=15)])

    enabled = BooleanField("Habilitado", default=True)

    system_admin = BooleanField("System Admin", default=False)


class UserCreateForm(UserManagementForm):
    current_email = None
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

    submit_another = SubmitField("Agregar otro")



class UserEditForm(UserManagementForm):

    def __init__(self, *args, **kwargs):
        self.current_email = kwargs.pop("current_email", None)
        super(UserEditForm, self).__init__(*args, **kwargs)


class UserSearchForm(FlaskForm):
    class Meta:
        csrf = False

    search_by = SelectField(
        choices=[
            ("email", "Email"),
        ],
        validate_choice=True,
    )
    search_text = StringField(validators=[Length(max=50)])

    filter_enabled = SelectField(
        choices=[
            ("true", "Si"),
            ("false", "No"),
            ("", "Todos"),
        ],
        validate_choice=True,
    )

    filter_role_id = SelectField(
        choices=[("", "Todos")]
        + [(str(index + 1), role.value) for index, role in enumerate(RoleEnum)],
    )

    order_by = SelectField(
        choices=[
            ("id", "ID"),
            ("email", "Email"),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[("asc", "Ascendente"), ("desc", "Descendente")], validate_choice=True
    )
    submit_search = SubmitField("Buscar")


class AccountSearchForm(FlaskForm):
    search_text = StringField(
        "Buscar por nombre o email", validators=[Length(message="Debe ingresar un texto", min=1, max=50)]
    )
    submit_search = SubmitField("Buscar")

class AccountSelectForm(FlaskForm):
    selected_account = HiddenField(
        "Cuenta seleccionada",
        validators=[DataRequired("Se debe seleccionar una cuenta"), IsNumber()],
    )
    submit_account = SubmitField("Asociar")

    def set_selected_account(self, account_id):
        self.selected_account.data = account_id