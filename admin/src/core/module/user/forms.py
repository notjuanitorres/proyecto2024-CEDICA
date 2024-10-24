"""
forms.py

This module defines various forms used in the user management system, including forms
for creating, editing, and searching users, as well as handling account selection.
It leverages WTForms and Flask-WTF for form handling and validation.
"""

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
from src.core.module.common.forms import BaseSearchForm
from ..common import IsValidName


def email_existence(form, field):
    """
    Check if the email is assigned to another user.

    Args:
        form: The form object that includes the field.
        field: The field object representing the email input.
    """
    validator = EmailExistence(message="Email en uso")
    validator(form, field)


class UserManagementForm(FlaskForm):
    """
    Base form for managing user information, including role, email, alias, and system admin status.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the UserManagementForm.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(UserManagementForm, self).__init__(*args, **kwargs)
        self.role_id.choices = self.get_role_choices()

    def get_role_choices(self):
        """
        Get the choices for the role select field.

        Returns:
            list: A list of tuples containing role IDs and role names.
        """
        return [(role.id, role.name) for role in self.import_validator().get_roles()]

    def import_validator(self):
        """
        Import the validator dynamically at runtime.

        Returns:
            The auth services container.
        """
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
    """
    Form for creating a new user, including password and confirm password fields.
    """

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
    """
    Form for editing an existing user, including the current email field.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the UserEditForm.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.current_email = kwargs.pop("current_email", None)
        super(UserEditForm, self).__init__(*args, **kwargs)


class UserSearchForm(BaseSearchForm):
    """
    Form for searching users based on various criteria, including email and role.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the UserSearchForm.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
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
    """
    Form for searching accounts by name or email.
    """

    search_text = StringField(
        "Buscar por nombre o email", validators=[Length(message="Debe ingresar un texto", min=1, max=50)]
    )
    submit_search = SubmitField("Buscar")


class AccountSelectForm(FlaskForm):
    """
    Form for selecting an account.

    Fields:
        selected_account (HiddenField): The selected account's ID.
        submit_account (SubmitField): The button to submit the account selection.
    """

    selected_item = HiddenField(
        "Cuenta seleccionada",
        validators=[DataRequired("Se debe seleccionar una cuenta"), IsNumber()],
    )
    submit_item = SubmitField("Asociar")

    def set_selected_account(self, account_id):
        """
        Set the selected account ID.

        Args:
            account_id: The ID of the selected account.
        """
        self.selected_item.data = account_id
