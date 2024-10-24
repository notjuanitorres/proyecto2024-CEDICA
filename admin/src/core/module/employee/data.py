"""
enums.py

This module defines enumerations for various classifications related to
employee management within the organization.

Enumerations defined in this module:
- ProfessionsEnum: Represents various professions relevant to employees.
- JobPositionEnum: Defines different job positions employees can hold.
- JobConditionEnum: Specifies various conditions of employment.
- FileTagEnum: Identifies types of documents associated with employees.
"""
from enum import Enum


class ProfessionsEnum(Enum):
    """
    An enumeration representing various professions.

    Each member of this enumeration corresponds to a specific profession
    relevant to the employee model in the system.
    """

    PSICOLOGO = "Psicólogo/a"
    PSICOMOTRICISTA = "Psicomotricista"
    MEDICO = "Médico/a"
    KINESIOLOGO = "Kinesiólogo/a"
    TERAPISTA_OCUPACIONAL = "Terapista Ocupacional"
    PSICOPEDAGOGO = "Psicopedagogo/a"
    DOCENTE = "Docente"
    PROFESOR = "Profesor"
    FONOAUDIOLOGO = "Fonoaudiólogo/a"
    VETERINARIO = "Veterinario/a"
    OTRO = "Otro"


class JobPositionEnum(Enum):
    """
    An enumeration representing various job positions.

    Each member of this enumeration corresponds to a specific job position
    that an employee may hold within the organization.
    """

    ADMINISTRATIVO = "Administrativo/a"
    TERAPEUTA = "Terapeuta"
    CONDUCTOR = "Conductor"
    AUXILIAR_PISTA = "Auxiliar de pista"
    HERRERO = "Herrero"
    VETERINARIO = "Veterinario"
    ENTRENADOR_CABALLOS = "Entrenador de Caballos"
    DOMADOR = "Domador"
    PROFESOR_EQUITACION = "Profesor de Equitación"
    DOCENTE_CAPACITACION = "Docente de Capacitación"
    AUXILIAR_MANTENIMIENTO = "Auxiliar de mantenimiento"
    OTRO = "Otro"


class JobConditionEnum(Enum):
    """
    An enumeration representing various job conditions.

    Each member of this enumeration defines a type of employment condition
    applicable to the employees.
    """

    VOLUNTARIO = "Voluntario"
    PERSONAL_RENTADO = "Personal Rentado"
    OTRO = "Otro"


class FileTagEnum(Enum):
    """
    An enumeration representing various file tags.

    Each member of this enumeration corresponds to a specific type of
    document associated with an employee.
    """

    DNI = "DNI"
    TITLE = "Titulo"
    CURRICULUM_VITAE = "Curriculum Vitae"


employment_enums = {
    "professions": ProfessionsEnum,
    "positions": JobPositionEnum,
    "conditions": JobConditionEnum,
}
