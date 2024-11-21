from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import Length, DataRequired, Optional
from src.core.module.publication.models import EstadoPublicacionEnum, TipoPublicacionEnum
from flask_ckeditor import CKEditorField


class PublicationSearchForm(FlaskForm):
    """
    Form for searching publications based on various criteria, including title, author, status, and date range.

    Fields:
        search_by (SelectField): Criteria to search by (e.g., title, author).
        search_text (StringField): The text input for searching publications.
        filter_status (SelectField): Filter by publication status.
        filter_type (SelectField): Filter by publication type.
        start_date (DateField): The start date for the search range.
        end_date (DateField): The end date for the search range.
        order_by (SelectField): Criteria to order the search results.
        order (SelectField): Order direction (ascendente or descendente).
        submit_search (SubmitField): The button to submit the search.
    """

    class Meta:
        """Metaclass to disable CSRF protection."""
        csrf = False

    search_by = SelectField(
        choices=[
            ("title", "Título"),
            ("alias", "Autor"),
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
        choices=[("", "Ver Todas")] + [(s.name, s.value) for s in EstadoPublicacionEnum],
        validate_choice=True,
    )

    filter_type = SelectField(
        "Tipo",
        choices=[("", "Ver Todas")] + [(t.name, t.value) for t in TipoPublicacionEnum],
        validate_choice=True,
    )

    start_date = DateField("Fecha de inicio", format='%Y-%m-%d')
    end_date = DateField("Fecha de fin", format='%Y-%m-%d')

    order_by = SelectField(
        choices=[
            ("id", "ID"),
            ("title", "Título"),
            ("publish_date", "Fecha de publicación"),
            ("create_date", "Fecha de creación"),
            ("update_date", "Fecha de actualización"),
        ],
        validate_choice=True,
    )
    order = SelectField(
        choices=[("asc", "Ascendente"), ("desc", "Descendente")],
        validate_choice=True
    )
    submit_search = SubmitField("Buscar")

    def validate(self, **kwargs):
        """
        Custom validation function to ensure valid date range selection.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: True if validation passes, False otherwise.
        """

        # Don't validate dates if no search is submitted
        if not self.start_date.data or not self.end_date.data:
            return True

        # Ensure end date >= start date
        if self.start_date.data > self.end_date.data:
            self.start_date.errors = []
            self.start_date.errors.append('La fecha de inicio no puede ser mayor a la fecha de fin.')
            return False

        return True


class PublicationManagementForm(FlaskForm):
    """
    Base form for managing publication information, including title, summary, content, and status.

    Fields:
        title (StringField): The title of the publication.
        summary (StringField): A brief summary of the publication.
        content (TextAreaField): The main content of the publication.
        status (SelectField): The status of the publication.
    """

    title = StringField(
        "Título",
        validators=[
            DataRequired(message="El título es obligatorio."),
            Length(max=255, message="El título no puede superar los 255 caracteres")
        ]
    )
    summary = StringField(
        "Resumen",
        validators=[
            Optional(),
            Length(max=255, message="El resumen no puede superar los 255 caracteres")
        ]
    )
    content = CKEditorField(
        "Contenido",
        validators=[
            DataRequired(message="El contenido es obligatorio.")
        ]
    )
    status = SelectField(
        "Estado",
        choices=[(s.name, s.value) for s in EstadoPublicacionEnum],
        validate_choice=True,
        validators=[DataRequired(message="El estado es obligatorio.")],
    )
    type = SelectField(
        "Tipo",
        choices=[(t.name, t.value) for t in TipoPublicacionEnum],
        validate_choice=True,
        validators=[DataRequired(message="El tipo es obligatorio.")],
    )


class PublicationCreateForm(PublicationManagementForm):
    """
    Form for creating a new publication.

    Inherits all fields from PublicationManagementForm.
    """

    pass


class PublicationEditForm(PublicationManagementForm):
    """
    Form for editing an existing publication.

    Inherits all fields from PublicationManagementForm.
    """
    pass
