def format_date(value, date_format='%d/%m/%Y %H:%M'):
    return value.strftime(date_format)

    
def render_natural_boolean(value):
    return 'Si' if value else 'No'


def render_role(role_id: int):
    roles = {
        1: "Admin",
        2: "Voluntario",
        3: "Ecuestre",
        4: "Técnico",
    }
    return roles.get(role_id, "No definido")


def register_filters(app):
    app.jinja_env.filters['natural_boolean'] = render_natural_boolean
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['role'] = render_role
    