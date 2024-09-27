from src.web.controllers import index_bp, users_bp, auth_bp, equestrian_bp


def register_blueprints(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(equestrian_bp)
