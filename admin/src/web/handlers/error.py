from flask import Blueprint, render_template


errors_bp = Blueprint("errors", __name__, template_folder="../templates/error/")


@errors_bp.app_errorhandler(400)
def bad_request_error(error):
    return render_template("4xx/400.html", error=error), 400


@errors_bp.app_errorhandler(401)
def unauthorized_error(error):
    return render_template("4xx/401.html", error=error), 401


@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template("4xx/403.html", error=error), 403


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("4xx/404.html", error=error), 404


@errors_bp.app_errorhandler(405)
def method_not_allowed_error(error):
    return render_template("4xx/405.html", error=error), 405


@errors_bp.app_errorhandler(500)
def internal_error(error):
    return render_template("5xx/500.html", error=error), 500


@errors_bp.app_errorhandler(502)
def bad_gateway_error(error):
    return render_template("5xx/502.html", error=error), 502

