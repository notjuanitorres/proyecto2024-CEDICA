from src.web.controllers import index_bp, auth_bp, users_bp, employee_bp, equestrian_bp, jockey_amazon_bp


def register_blueprints(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(equestrian_bp)
    app.register_blueprint(jockey_amazon_bp)
