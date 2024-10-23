from datetime import datetime
from sqlalchemy.orm import column_property 
from src.core.database import db
from src.core.module.common import AddressMixin, EmergencyContactMixin, PhoneMixin, File
from src.core.module.employee.data import (
    ProfessionsEnum,
    JobPositionEnum as PositionEnum,
    JobConditionEnum as ConditionEnum,
)


class EmployeeFile(File):
    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    owner = db.relationship("Employee", back_populates="files")


class Employee(db.Model, AddressMixin, PhoneMixin, EmergencyContactMixin):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    fullname = column_property(name + " " + lastname)
    dni = db.Column(db.String(10), nullable=False, unique=True)
    profession = db.Column(db.Enum(ProfessionsEnum), nullable=False)
    position = db.Column(db.Enum(PositionEnum), nullable=False)
    job_condition = db.Column(db.Enum(ConditionEnum), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.today())
    end_date = db.Column(db.Date, nullable=True)
    health_insurance = db.Column(db.Text, nullable=True)
    affiliate_number = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("User", backref=db.backref("employee", uselist=False))
    files = db.relationship("EmployeeFile", back_populates="owner", cascade="all, delete-orphan")
    horse_trainings = db.relationship("HorseTrainers", back_populates="employee", cascade="all, delete-orphan")
    charges = db.relationship("Charge", back_populates="employee", lazy="select")
