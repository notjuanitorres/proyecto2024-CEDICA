"""
enums.py

This module defines enumerations for various classifications related to
jockey and amazon management within the organization.

Enumerations defined in this module:
- DisabilityDiagnosisEnum: Represents various disability diagnoses
- DisabilityTypeEnum: Defines different types of disabilities
- FamilyAssignmentEnum: Specifies types of family benefits
- PensionEnum: Types of pensions available
- WorkProposalEnum: Different work proposals offered
- WorkConditionEnum: Work condition statuses
- SedeEnum: Organization locations
- DayEnum: Days of the week
- EducationLevelEnum: Educational levels
- FileTagEnum: Document classification tags
"""

from enum import Enum

class DisabilityDiagnosisEnum(Enum):
    """
    An enumeration representing various disability diagnoses.
    
    Each member corresponds to a specific medical diagnosis that may be
    associated with a jockey or amazon in the system. This comprehensive
    list covers various conditions from physical to developmental disabilities.
    """

    NO_DIAGNOSIS = "Sin diagnóstico"
    ECNE = "ECNE"
    POST_TRAUMATIC_INJURY = "Lesión post-traumática"
    MIOLOMENINGOCELE = "Mielomeningocele"
    MULTIPLE_SCLEROSIS = "Esclerosis Múltiple"
    MILD_SCOLIOSIS = "Escoliosis Leve"
    SEQUELAE_OF_CVA = "Secuelas de ACV"
    INTELLECTUAL_DISABILITY = "Discapacidad Intelectual"
    AUTISM_SPECTRUM_DISORDER = "Trastorno del Espectro Autista"
    LEARNING_DISORDER = "Trastorno del Aprendizaje"
    ADHD = "Trastorno por Déficit de Atención/Hiperactividad"
    COMMUNICATION_DISORDER = "Trastorno de la Comunicación"
    ANXIETY_DISORDER = "Trastorno de Ansiedad"
    DOWN_SYNDROME = "Síndrome de Down"
    DEVELOPMENTAL_DELAY = "Retraso Madurativo"
    PSYCHOSIS = "Psicosis"
    BEHAVIOR_DISORDER = "Trastorno de Conducta"
    MOOD_DISORDER = "Trastornos del ánimo y afectivos"
    EATING_DISORDER = "Trastorno Alimentario"
    OTHER = "OTRO"


class DisabilityTypeEnum(Enum):
    """
    An enumeration representing various types of disabilities.
    
    Each member represents a broad category of disability that can be
    used to classify the nature of a person's condition.
    """

    NONE = "No aplica"
    MENTAL = "Mental"
    MOTOR = "Motora"
    SENSORY = "Sensorial"
    VISCERAL = "Visceral"


class FamilyAssignmentEnum(Enum):
    """
    An enumeration representing types of family benefits.
    
    Each member corresponds to a specific type of family-related
    financial assistance that may be available to jockeys and amazons.
    """

    UNIVERSAL_WITH_CHILD = "Asignación Universal por hijo"
    UNIVERSAL_WITH_DISABLED_CHILD = "Asignación Universal por hijo con Discapacidad"
    ANNUAL_SCHOOL_HELP = "Asignación por ayuda escolar anual"


class PensionEnum(Enum):
    """
    An enumeration representing types of pensions.
    
    Each member represents a category of pension that may be
    available to jockeys and amazons.
    """

    PROVINCIAL = "Provincial"
    NATIONAL = "Nacional"


class WorkProposalEnum(Enum):
    """
    An enumeration representing various work proposals.
    
    Each member corresponds to a specific type of activity or service
    that can be offered within the organization's programs.
    """

    HIPOTHERAPY = "Hipoterapia"
    THERAPEUTIC_RIDING = "Monta Terapéutica"
    ADAPTED_EQUESTRIAN_SPORTS = "Deporte Ecuestre Adaptado"
    RECREATIONAL_ACTIVITIES = "Actividades Recreativas"
    RIDING = "Equitación"


class WorkConditionEnum(Enum):
    """
    An enumeration representing work condition statuses.
    
    Each member represents a possible status of a jockey or amazon's
    work condition within the organization.
    """

    REGULAR = "Regular"
    DISMISSED = "De baja"


class SedeEnum(Enum):
    """
    An enumeration representing organization locations.
    
    Each member corresponds to a specific location or branch
    where activities can take place.
    """

    CASJ = "CASJ"
    HLP = "HLP"
    OTHER = "OTRO"


class DayEnum(Enum):
    """
    An enumeration representing days of the week.
    
    Each member corresponds to a day when activities can be scheduled.
    Includes a mapping dictionary for abbreviated day codes.
    """   

    MONDAY = "Lunes"
    TUESDAY = "Martes"
    WEDNESDAY = "Miércoles"
    THURSDAY = "Jueves"
    FRIDAY = "Viernes"
    SATURDAY = "Sábado"
    SUNDAY = "Domingo"


DAYS_MAPPING = {
    'M': DayEnum.MONDAY,
    'O': DayEnum.TUESDAY,
    'N': DayEnum.WEDNESDAY,
    'D': DayEnum.THURSDAY,
    'A': DayEnum.FRIDAY,
    'Y': DayEnum.SATURDAY
}

class EducationLevelEnum(Enum):
    """
    An enumeration representing educational levels.
    
    Each member corresponds to a level of education that can be
    associated with a jockey or amazon's academic background.
    """

    PRIMARY = "Primario"
    SECONDARY = "Secundario"
    TERTIARY = "Terciario"
    UNIVERSITY = "Universitario"


jockey_amazon_enums = {
    "disability_diagnosis": DisabilityDiagnosisEnum,
    "disability_type": DisabilityTypeEnum,
    "family_assignment": FamilyAssignmentEnum,
    "pension": PensionEnum,
    "work_proposal": WorkProposalEnum,
    "work_condition": WorkConditionEnum,
    "sede": SedeEnum,
    "day": DayEnum,
    "education_level": EducationLevelEnum,
}


class FileTagEnum(Enum):
    """
    An enumeration representing document classification tags.
    
    Each member corresponds to a specific type of document that can be
    associated with a jockey or amazon's record.
    """

    ENTREVISTA = "entrevista"
    EVALUACION = "evaluación"
    PLANIFICACIONES = "planificaciones"
    EVOLUCION = "evolución"
    CRONICAS = "crónicas"
    DOCUMENTAL = "documental"
