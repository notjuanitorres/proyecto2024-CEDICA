"""
models.py

This module defines the SQLAlchemy models for managing employee records 
and associated file storage within the application. It includes the 
Employee and EmployeeFile classes, which represent the data structure 
for employees and their related documents.

Models:
- EmployeeFile: Represents files associated with employees, using it with 
  polymorphic behavior for different file types in the Files table.
- Employee: Represents an employee's personal and employment information, 
  including contact details, employment conditions, and associated files.
"""

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
    """
    Represents a file associated with an employee.

    This class extends the File class as a polymorphic child
    and includes a foreign key reference  to the Employee model, 
    enabling the association of multiple files with a single employee.
    """
    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id", ondelete="CASCADE"))
    owner = db.relationship("Employee", back_populates="files")


class Employee(db.Model, AddressMixin, PhoneMixin, EmergencyContactMixin):
    """
    Represents an employee's personal and employment information.

    This class contains details such as the employee's name, contact 
    information, job position, employment condition, and associated files. 
    It also implements mixins for address, phone, and emergency contact 
    details.
    """
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
