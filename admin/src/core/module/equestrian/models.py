from src.core.module.common.models import File
from src.core.database import db
from datetime import datetime
from enum import Enum as pyEnum


class JAEnum(pyEnum):
    """
    Enumeration for different types of J&A activities.

    Attributes:
        HIPOTHERAPY (str): Hipoterapia.
        THERAPEUTIC_RIDING (str): Monta Terapéutica.
        ADAPTED_SPORTS (str): Deporte Ecuestre Adaptado.
        RECREATIONAL_ACTIVITIES (str): Actividades Recreativas.
        RIDING (str): Equitación.
    """
    HIPOTHERAPY = "Hipoterapia"
    THERAPEUTIC_RIDING = "Monta Terapéutica"
    ADAPTED_SPORTS = "Deporte Ecuestre Adaptado"
    RECREATIONAL_ACTIVITIES = "Actividades Recreativas"
    RIDING = "Equitación"


class Horse(db.Model):
    """
        Model representing a horse.

        Attributes:
            id (int): The unique identifier of the horse.
            name (str): The name of the horse.
            birth_date (datetime.date): The birthdate of the horse.
            sex (str): The sex of the horse.
            breed (str): The breed of the horse.
            coat (str): The coat color of the horse.
            is_donation (bool): Indicates if the horse is a donation.
            admission_date (datetime.date): The admission date of the horse.
            assigned_facility (str): The facility assigned to the horse.
            ja_type (JAEnum): The type of J&A assigned to the horse.
            files (List[HorseFile]): The list of files related to the horse.
            is_archived (bool): Indicates if the horse is deleted.
            inserted_at (datetime.datetime): The timestamp when the horse was inserted.
            updated_at (datetime.datetime): The timestamp when the horse was last updated.
        """

    __tablename__ = 'horses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    coat = db.Column(db.String(100), nullable=False)
    is_donation = db.Column(db.Boolean, default=False)
    admission_date = db.Column(db.Date, nullable=False)
    assigned_facility = db.Column(db.String(100), nullable=False)
    ja_type = db.Column(db.Enum(JAEnum), nullable=False)
    files = db.relationship("HorseFile", back_populates="owner", cascade="all, delete-orphan")
    trainers = db.relationship("HorseTrainers", back_populates="horse", cascade="all, delete-orphan")
    work_assignments = db.relationship("WorkAssignment", back_populates="horse")
    is_archived = db.Column(db.Boolean, default=False)

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class HorseTrainers(db.Model):
    __tablename__ = 'horse_trainers'

    id = db.Column(db.Integer, primary_key=True)
    id_horse = db.Column(db.Integer, db.ForeignKey('horses.id', ondelete='CASCADE'))
    id_employee = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))

    horse = db.relationship("Horse", back_populates="trainers")
    employee = db.relationship("Employee", back_populates="horse_trainings")


class FileTagEnum(pyEnum):
    FICHA_GENERAL = "Ficha general del caballo"
    PLANIFICACION_ENTRENAMIENTO = "Planificación de Entrenamiento"
    INFORME_EVOLUCION = "Informe de Evolución"
    CARGA_IMAGENES = "Carga de Imágenes"
    REGISTRO_VETERINARIO = "Registro veterinario"


class HorseFile(File):
    __mapper_args__ = {
        "polymorphic_identity": "horse",
    }

    horse_id = db.Column(db.Integer, db.ForeignKey("horses.id", ondelete='CASCADE'))
    owner = db.relationship("Horse", back_populates="files")
