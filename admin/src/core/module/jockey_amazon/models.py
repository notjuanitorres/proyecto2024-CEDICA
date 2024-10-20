from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import backref

from src.core.module.common import File
from src.core.database import db
from src.core.module.common import AddressMixin, EmergencyContactMixin, PhoneMixin


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


class SchoolInstitution(db.Model):
    __tablename__ = 'school_institutions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(50), nullable=True)
    locality = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    phone_country_code = db.Column(db.String(5), nullable=False)
    phone_area_code = db.Column(db.String(5), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)


class FamilyMember(db.Model):
    __tablename__ = 'family_members'

    id = db.Column(db.Integer, primary_key=True)
    relationship = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    street = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(50), nullable=True)
    locality = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    phone_country_code = db.Column(db.String(5), nullable=False)
    phone_area_code = db.Column(db.String(5), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    education_level = db.Column(SQLAEnum(EducationLevelEnum), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)

    jockey_amazon = db.relationship('JockeyAmazon', secondary='family_member_jockey_amazon',
                                    back_populates='family_members')


class WorkAssignment(db.Model):
    __tablename__ = 'work_assignments'

    id = db.Column(db.Integer, primary_key=True)
    proposal = db.Column(SQLAEnum(WorkProposalEnum), nullable=False)
    condition = db.Column(SQLAEnum(WorkConditionEnum), nullable=False)
    sede = db.Column(SQLAEnum(SedeEnum), nullable=False)
    days = db.Column(db.ARRAY(SQLAEnum(DayEnum)), nullable=False)

    professor_or_therapist_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    conductor_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    track_assistant_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'), nullable=True)
    horse = db.relationship('Horse')

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    professor_or_therapist = db.relationship('Employee', foreign_keys=[professor_or_therapist_id],
                                             backref='work_assignments_as_professor_or_therapist')
    conductor = db.relationship('Employee', foreign_keys=[conductor_id], backref='work_assignments_as_conductor')
    track_assistant = db.relationship('Employee', foreign_keys=[track_assistant_id],
                                      backref='work_assignments_as_track_assistant')


class JockeyAmazon(db.Model, AddressMixin, PhoneMixin, EmergencyContactMixin):
    __tablename__ = 'jockeys_amazons'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.String(100), nullable=False)
    has_debts = db.Column(db.Boolean, default=False)

    has_scholarship = db.Column(db.Boolean, default=False)
    scholarship_observations = db.Column(db.Text, nullable=True)
    scholarship_percentage = db.Column(db.Float, nullable=True)

    has_disability = db.Column(db.Boolean, default=False)
    disability_diagnosis = db.Column(SQLAEnum(DisabilityDiagnosisEnum), nullable=True)
    disability_other = db.Column(db.String(100), nullable=True)
    disability_type = db.Column(SQLAEnum(DisabilityTypeEnum), nullable=True)

    has_family_assignment = db.Column(db.Boolean, default=False)
    family_assignment_type = db.Column(SQLAEnum(FamilyAssignmentEnum), nullable=True)

    has_pension = db.Column(db.Boolean, default=False)
    pension_type = db.Column(SQLAEnum(PensionEnum), nullable=True)
    pension_details = db.Column(db.String(100), nullable=True)

    social_security = db.Column(db.String(100), nullable=True)
    social_security_number = db.Column(db.String(50), nullable=True)
    has_curatorship = db.Column(db.Boolean, default=False)
    curatorship_observations = db.Column(db.Text, nullable=True)

    school_institution_id = db.Column(db.Integer, db.ForeignKey('school_institutions.id'), nullable=True)
    school_institution = db.relationship('SchoolInstitution')

    current_grade_year = db.Column(db.String(50), nullable=True)
    school_observations = db.Column(db.Text, nullable=True)

    professionals = db.Column(db.Text, nullable=True)

    family_members = db.relationship('FamilyMember', secondary='family_member_jockey_amazon',
                                     back_populates='jockey_amazon')
    work_assignment_id = db.Column(db.Integer, db.ForeignKey('work_assignments.id'), nullable=True)
    work_assignment = db.relationship('WorkAssignment')

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    family_member_jockey_amazon = db.Table('family_member_jockey_amazon',
                                           db.Column('family_member_id', db.Integer, db.ForeignKey('family_members.id'),
                                                     primary_key=True),
                                           db.Column('jockey_amazon_id', db.Integer,
                                                     db.ForeignKey('jockeys_amazons.id'), primary_key=True)
                                           )
    files = db.relationship("JockeyAmazonFile", back_populates="owner")
    charges = db.relationship("Charge", back_populates="jya", lazy="select")


class JockeyAmazonFile(File):
    __mapper_args__ = {
        "polymorphic_identity": "jockey_amazon",
    }

    jockey_amazon_id = db.Column(db.Integer, db.ForeignKey("jockeys_amazons.id"))
    owner = db.relationship("JockeyAmazon", back_populates="files")
