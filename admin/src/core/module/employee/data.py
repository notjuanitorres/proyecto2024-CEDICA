from enum import Enum


class ProfessionsEnum(Enum):
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
    VOLUNTARIO = "Voluntario"
    PERSONAL_RENTADO = "Personal Rentado"
    OTRO = "Otro"


class FileTagEnum(Enum):
    DNI = "DNI"
    TITLE = "Titulo"
    CURRICULUM_VITAE = "Curriculum Vitae"


employment_enums = {
    "professions": ProfessionsEnum,
    "positions": JobPositionEnum,
    "conditions": JobConditionEnum,
}
