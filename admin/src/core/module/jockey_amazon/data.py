from enum import Enum

class DisabilityDiagnosisEnum(Enum):
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
    MENTAL = "Mental"
    MOTOR = "Motora"
    SENSORY = "Sensorial"
    VISCERAL = "Visceral"


class FamilyAssignmentEnum(Enum):
    UNIVERSAL_WITH_CHILD = "Asignación Universal por hijo"
    UNIVERSAL_WITH_DISABLED_CHILD = "Asignación Universal por hijo con Discapacidad"
    ANNUAL_SCHOOL_HELP = "Asignación por ayuda escolar anual"


class PensionEnum(Enum):
    PROVINCIAL = "Provincial"
    NATIONAL = "Nacional"


class WorkProposalEnum(Enum):
    HIPOTHERAPY = "Hipoterapia"
    THERAPEUTIC_RIDING = "Monta Terapéutica"
    ADAPTED_EQUESTRIAN_SPORTS = "Deporte Ecuestre Adaptado"
    RECREATIONAL_ACTIVITIES = "Actividades Recreativas"
    RIDING = "Equitación"


class WorkConditionEnum(Enum):
    REGULAR = "Regular"
    DISMISSED = "De baja"


class SedeEnum(Enum):
    CASJ = "CASJ"
    HLP = "HLP"
    OTHER = "OTRO"


class DayEnum(Enum):
    MONDAY = "Lunes"
    TUESDAY = "Martes"
    WEDNESDAY = "Miércoles"
    THURSDAY = "Jueves"
    FRIDAY = "Viernes"
    SATURDAY = "Sábado"
    SUNDAY = "Domingo"


class EducationLevelEnum(Enum):
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
    ENTREVISTA = "entrevista"
    EVALUACION = "evaluación"
    PLANIFICACIONES = "planificaciones"
    EVOLUCION = "evolución"
    CRONICAS = "crónicas"
    DOCUMENTAL = "documental"
