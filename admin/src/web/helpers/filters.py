def format_date(value, date_format='%d/%m/%Y %H:%M'):
    return value.strftime(date_format)


def render_natural_boolean(value):
    return 'Si' if value else 'No'


def render_role(role_id: int):
    roles = {
        1: "Técnico",
        2: "Ecuestre",
        3: "Voluntario",
        4: "Administración",
    }
    return roles.get(role_id, "No definido")


def render_file_type(is_link: bool):
    return '(Url)' if is_link else '(Archivo)'


def register_filters(app):
    app.jinja_env.filters['natural_boolean'] = render_natural_boolean
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['role'] = render_role
    app.jinja_env.filters['file_type'] = render_file_type
