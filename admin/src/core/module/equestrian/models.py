from src.core.database import db
from datetime import datetime

from enum import Enum as pyEnum


class JAEnum(pyEnum):
    HIPOTHERAPY = "Hipoterapia"
    THERAPEUTIC_RIDING = "Monta Terapéutica"
    ADAPTED_SPORTS = "Deporte Ecuestre Adaptado"
    RECREATIONAL_ACTIVITIES = "Actividades Recreativas"
    RIDING = "Equitación"


class Horse(db.Model):
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

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)


class HorseTrainers(db.Model):
    __tablename__ = 'horse_trainers'

    id = db.Column(db.Integer, primary_key=True)
    id_horse = db.Column(db.Integer, db.ForeignKey('horses.id'))
    # TODO: uncomment this when members table is created
    # id_trainer = db.Column(db.Integer, db.ForeignKey('members.id'))
