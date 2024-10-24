from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize, FileRequired
from wtforms import (
    FileField,
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
from src.core.module.common.forms import BaseSearchForm
from ..common import IsValidName


def email_existence(form, field):
    validator = EmailExistence(message="Email en uso")
    validator(form, field)

def max_file_size(size_in_mb: int):
    BYTES_PER_MB = 1024 * 1024

    size_in_bytes = size_in_mb * BYTES_PER_MB
    return size_in_bytes

allowed_filetypes = ["pdf", "jpg", "jpeg", "png", "webp"]
formatted_filetypes = ", ".join(f".{ext}" for ext in allowed_filetypes[:-1]) + f" y .{allowed_filetypes[-1]}"
filetypes_message = f"Formato no reconocido. Formato válido: {formatted_filetypes}"

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
        validate_choice=True,
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
    alias = StringField("Alias", validators=[DataRequired(), Length(min=3, max=15), IsValidName()])

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
    profile_image = FileField('Cargar foto de perfil', 
            validators=[FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                upload_set=allowed_filetypes,
                message=filetypes_message,
            )] )
    def __init__(self, *args, **kwargs):
        self.current_email = kwargs.pop("current_email", None)
        super(UserEditForm, self).__init__(*args, **kwargs)


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
        validators=[Optional()]
    )

    filter_role_id = SelectField(
        choices=[("", "Todos")]
        + [(str(index + 1), role.value) for index, role in enumerate(RoleEnum)],
        validate_choice=True,
    )


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



class UserProfileForm(FlaskForm):
    email = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email(message="Email inválido"),
            Length(max=100),
        ],
    )
    alias = StringField("Alias", validators=[DataRequired(), Length(min=3, max=15)])
    profile_image = FileField('Cargar foto de perfil', 
            validators=[FileSize(
                max_size=max_file_size(size_in_mb=5),
                message="El archivo es demasiado grande",
            ),
            FileAllowed(
                upload_set=allowed_filetypes,
                message=filetypes_message,
            )] )
    current_password = PasswordField(
        "Contraseña actual",
        validators=[
            DataRequired(),
            Length(
                min=8, max=255, message="La contraseña debe tener más de 8 caracteres"
            ),
        ],
    )
    new_password = PasswordField(
        "Nueva contraseña",
        validators=[
            Optional(),
            Length(
                min=8, max=255, message="La contraseña debe tener más de 8 caracteres"
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar nueva contraseña",
        validators=[
            Optional(),
            EqualTo("new_password", message="Las contraseñas deben coincidir"),
        ],
    )
    submit = SubmitField("Guardar cambios")