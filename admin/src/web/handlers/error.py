from dataclasses import dataclass
from flask import render_template


@dataclass
class Error:
    """
        Data class representing an error.

        Attributes:
            code (int): The HTTP status code of the error.
            name (str): The name of the error.
            description (str): The description of the error.
        """
    code: int
    name: str
    description: str


def handle_error(e):
    """
        Handle HTTP errors and render an error template.

        Args:
            e (HTTPException): The HTTP exception.

        Returns:
            Response: The rendered error template and the HTTP status code.
        """
    error_map = {
        400: (
            "Solicitud incorrecta",
            "La solicitud no se pudo entender por el servidor debido a una sintaxis mal formada."),
        401: ("No autorizado", "No tiene autorización para acceder a este recurso."),
        403: ("Prohibido", "No tiene permiso para acceder a este recurso."),
        404: ("No encontrado", "La URL solicitada no se encuentra en el servidor."),
        405: ("Método no permitido", "El método no está permitido para la URL solicitada."),
        500: ("Error interno del servidor",
              "El servidor encontró una condición inesperada que le impidió completar la solicitud.")
    }

    code = e.code if e.code in error_map else 500
    name, description = error_map.get(code, ("Error desconocido", "Ocurrió un error inesperado."))

    error = Error(code, name, description)
    return render_template("error/error.html", error=error), code
