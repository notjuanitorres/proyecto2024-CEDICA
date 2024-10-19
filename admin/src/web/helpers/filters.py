def format_date(value, date_format='%d/%m/%Y %H:%M'):
    """
        Format a date value into a string based on the given date format.

        Args:
            value: The date value to format.
            date_format (str): The format string to use for formatting the date.

        Returns:
            str: The formatted date string.
        """
    return value.strftime(date_format)


def render_natural_boolean(value):
    """
        Render a boolean value as a natural language string.

        Args:
            value (bool): The boolean value to render.

        Returns:
            str: 'Si' if the value is True, otherwise 'No'.
        """
    return 'Si' if value else 'No'


def render_role(role_id: int):
    """
        Render a role ID as a role name.

        Args:
            role_id (int): The role ID to render.

        Returns:
            str: The role name corresponding to the role ID, or 'No definido' if the role ID is not found.
        """
    roles = {
        1: "Técnico",
        2: "Ecuestre",
        3: "Voluntario",
        4: "Administración",
    }
    return roles.get(role_id, "No definido")


def render_file_type(is_link: bool):
    """
        Render the file type based on whether it is a link or a file.

        Args:
            is_link (bool): True if the file is a link, otherwise False.

        Returns:
            str: '(Url)' if the file is a link, otherwise '(Archivo)'.
        """
    return '(Url)' if is_link else '(Archivo)'


def register_filters(app):
    """
        Register custom Jinja filters with the Flask application.

        Args:
            app (Flask): The Flask application instance.
        """
    app.jinja_env.filters['natural_boolean'] = render_natural_boolean
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['role'] = render_role
    app.jinja_env.filters['file_type'] = render_file_type
