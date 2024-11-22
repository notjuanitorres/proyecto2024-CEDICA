from flask import abort, Blueprint, render_template, request, url_for, session, redirect, flash
from flask_dance.contrib.google import make_google_blueprint, google
from dependency_injector.wiring import inject, Provide

from src.core.module.user import UserRepository
from src.core.container import Container
from src.core.module.user.mappers import UserMapper
from src.core.module.auth import AbstractAuthServices as AAS, UserLoginForm, UserRegisterForm
from src.web.helpers.auth import is_authenticated

auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="../templates/accounts", url_prefix="/auth"
)
google_bp = make_google_blueprint(
    scope=["openid", "profile", "email"],
    redirect_url="/auth/login/google/callback",  # Updated redirect URL
    authorized_url="/autorizado"
)
auth_bp.register_blueprint(google_bp, url_prefix="/login/google")


@inject
def create_session(user: dict, auth_services: AAS = Provide[Container.auth_services]):
    session["user"] = user["id"]
    session["user_name"] = user["alias"]
    session["is_authenticated"] = True
    session["is_admin"] = user["system_admin"]
    permissions = auth_services.get_permissions_of(user["id"])
    session["permissions"] = permissions


@auth_bp.route("/login/google")
def google_login():
    """
    Initial Google OAuth login route
    """
    if not google.authorized:
        return redirect(url_for("auth_bp.google.login"))
    return redirect(url_for("auth_bp.google_callback"))


@auth_bp.route("/login/google/callback")
def google_callback():
    """
    Handle Google OAuth callback and user verification
    """
    if not google.authorized:
        flash("Error en la autorización con Google", "danger")
        return redirect(url_for("auth_bp.login"))

    response = google.get("/oauth2/v2/userinfo")
    if not response.ok:
        flash("Error al obtener información de Google", "danger")
        return redirect(url_for("auth_bp.login"))

    google_info = response.json()
    return handle_google_login(google_info)


@inject
def handle_google_login(
        google_info: dict,
        auth_services: AAS = Provide[Container.auth_services],
        user_repository: UserRepository = Provide[Container.user_repository]
):
    """
    Handle Google OAuth login and registration flow

    Args:
        google_info (dict): User information from Google
        auth_services (AAS): The authentication services
        user_repository (UserRepository): The user repository services
    """
    email = google_info.get('email')
    if not email:
        flash("No se pudo obtener el email desde Google", "danger")
        return redirect(url_for("auth_bp.login"))

    user_exists = auth_services.validate_email(email)

    if not user_exists:
        # Store Google info in session and redirect to registration
        session['provider_information'] = google_info
        return redirect(url_for("auth_bp.register_with_provider"))

    user = user_repository.get_by_email(email)
    if not user:
        flash("Error al obtener información del usuario", "danger")
        return redirect(url_for("auth_bp.login"))

    if not user.enabled:
        flash("Tu cuenta está pendiente de activación por el administrador.", "warning")
        return redirect(url_for("auth_bp.login"))

    create_session(user.to_dict())
    flash("Sesión iniciada correctamente, bienvenido/a.", "success")
    return redirect(url_for("index_bp.home"))


@auth_bp.route("/registrarse/proveedor", methods=["GET", "POST"])
@inject
def register_with_provider(user_repository: AAS = Provide[Container.user_repository]):
    provider_data = session.get("provider_information", None)
    if not provider_data:
        abort(400)

    registration_form = UserRegisterForm(data={
        "email": provider_data.get("email"),
        "alias": f"{provider_data.get("given_name")} {provider_data.get("family_name")}"
    })

    if request.method == "POST":
        if not registration_form.validate_on_submit():
            return render_template("register_provider.html", form=registration_form)
        provider_id = provider_data.get("id")
        user_repository.add(UserMapper.to_entity(registration_form.data, provider_id=provider_id))
        del session['provider_information']
        flash("Registro exitoso.", "success")
        flash("Tienes que esperar a que el administrador del sistema te habilite el acceso para ingresar", "warning")
        return redirect(url_for("index_bp.home"))

    return render_template("register_provider.html", form=registration_form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Display the login form and handle login requests.

    If the user is already authenticated, redirect to the home page.
    If the request method is POST, authenticate the user.
    Otherwise, render the login form.

    Returns:
        A rendered template for the login form or a redirect to the home page.
    """
    if is_authenticated(session):
        return redirect(url_for("index_bp.home"))

    login_form = UserLoginForm()

    if request.method == "POST":
        return authenticate(login_form=login_form)

    return render_template("login.html", form=login_form)


@inject
def authenticate(login_form: UserLoginForm, auth_services: AAS = Provide[Container.auth_services]):
    """
    Authenticate the user based on the login form data.

    Args:
        login_form (UserLoginForm): The form containing the user's login data.
        auth_services (AAS): The authentication services.

    Returns:
        A rendered template for the login form if validation fails or authentication fails,
        or a redirect to the home page if authentication is successful.
    """
    if not login_form.validate_on_submit():
        return render_template("login.html", form=login_form)

    user = auth_services.authenticate(
        login_form.email.data, login_form.password.data
    )

    if not user:
        flash("Email o contraseña inválida", "danger")
        return render_template("login.html", form=login_form)

    create_session(user)

    flash("Sesión iniciada correctamente, bienvenido/a.", "success")

    return redirect(url_for("index_bp.home"))


@auth_bp.post("/logout")
def logout():
    """
    Log out the user by clearing the session.

    If the user is logged in, clear the session and flash a success message.
    Redirect to the home page.

    Returns:
        A redirect to the home page.
    """
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("Sesión cerrada", "success")

    return redirect(url_for("index_bp.home"))


@auth_bp.route("/registrarse", methods=["GET", "POST"])
def register():
    """
    Display the registration form and handle registration requests.

    If the user is already authenticated, flash an info message and redirect to the home page.
    If the request method is POST, register the user.
    Otherwise, render the registration form.

    Returns:
        A rendered template for the registration form or a redirect to the home page.
    """
    if is_authenticated(session):
        flash("Ya estás autenticado", "info")
        return redirect(url_for("index_bp.home"))

    registration_form = UserRegisterForm()

    if request.method == "POST":
        return register_user(registration_form=registration_form)

    return render_template("register.html", form=registration_form)


@inject
def register_user(registration_form: UserRegisterForm, user_repository: AAS = Provide[Container.user_repository]):
    """
    Register a new user based on the registration form data.

    Args:
        registration_form (UserRegisterForm): The form containing the user's registration data.
        user_repository (AAS): The user repository services.

    Returns:
        A rendered template for the registration form if validation fails,
        or a redirect to the home page if registration is successful.
    """
    if not registration_form.validate_on_submit():
        return render_template("register.html", form=registration_form)

    user_repository.add(UserMapper.to_entity(registration_form.data))
    flash("Registro exitoso.", "success")
    flash("Tienes que esperar a que el administrador del sistema te habilite el acceso para ingresar", "warning")
    return redirect(url_for("index_bp.home"))
