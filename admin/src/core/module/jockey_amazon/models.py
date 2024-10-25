"""
models.py

SQLAlchemy models for managing jockey and amazon-related data in the system.

This module defines the database schema and relationships for jockeys, their family members,
work assignments, school information, and related entities. It uses SQLAlchemy ORM for
database interactions and includes various mixins for common fields.

Models:
    - SchoolInstitution: Educational institution details
    - FamilyMember: Family member information
    - WorkAssignment: Work and assignment details
    - JockeyAmazon: Main jockey/amazon information
    - JockeyAmazonFile: File attachments for jockeys/amazons
"""

from datetime import datetime
from sqlalchemy import Enum as SQLAEnum

from src.core.module.common import File
from src.core.module.common import AddressMixin, EmergencyContactMixin, PhoneMixin
from src.core.database import db
from .data import (
    DisabilityDiagnosisEnum,
    DisabilityTypeEnum,
    FamilyAssignmentEnum,
    PensionEnum,
    WorkProposalEnum,
    WorkConditionEnum,
    SedeEnum,
    DayEnum,
    EducationLevelEnum,
)


class SchoolInstitution(db.Model):
    """
    Educational institution information associated with a jockey/amazon.

    This model stores details about the educational institution including
    contact information and address details.

    Attributes:
        id (int): Primary key
        name (str): Institution name, max length 200
        street (str): Street address, max length 50
        number (int): Street number
        department (str): Department/unit, optional, max length 50
        locality (str): City/locality, max length 50
        province (str): Province/state, max length 50
        phone_country_code (str): Country code for phone, max length 5
        phone_area_code (str): Area code for phone, max length 5
        phone_number (str): Phone number, max length 15
        jockey_amazon_id (int): Foreign key to JockeyAmazon
        jockey_amazon (JockeyAmazon): Relationship to associated jockey/amazon
    """

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
    jockey_amazon_id = db.Column(db.Integer, db.ForeignKey('jockeys_amazons.id', ondelete='CASCADE'), nullable=False)
    jockey_amazon = db.relationship('JockeyAmazon',
                                    back_populates='school_institution',
                                    uselist=False)


class FamilyMember(db.Model):
    """
    Family member information for a jockey/amazon.

    This model stores personal and contact information for family members,
    including their relationship to the jockey/amazon and educational background.

    Attributes:
        id (int): Primary key
        relationship (str): Relationship to jockey/amazon, max length 50
        first_name (str): First name, max length 100
        last_name (str): Last name, max length 100
        dni (str): Unique national ID number, max length 20
        street (str): Street address, max length 50
        number (int): Street number
        department (str): Department/unit, optional, max length 50
        locality (str): City/locality, max length 50
        province (str): Province/state, max length 50
        phone_country_code (str): Country code for phone, max length 5
        phone_area_code (str): Area code for phone, max length 5
        phone_number (str): Phone number, max length 15
        email (str): Email address, max length 100
        education_level (EducationLevelEnum): Education level
        occupation (str): Current occupation, max length 100
        jockey_amazon_id (int): Foreign key to JockeyAmazon
        jockey_amazon (JockeyAmazon): Relationship to associated jockey/amazon
    """

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
    jockey_amazon_id = db.Column(db.Integer, db.ForeignKey('jockeys_amazons.id', ondelete='CASCADE'), nullable=False)
    jockey_amazon = db.relationship('JockeyAmazon',
                                    back_populates='family_members')


class WorkAssignment(db.Model):
    """
    Work assignment details for a jockey/amazon.

    This model tracks work assignments including schedule, location, and associated
    staff members such as professors, conductors, and track assistants.

    Attributes:
        id (int): Primary key
        proposal (WorkProposalEnum): Type of work proposal
        condition (WorkConditionEnum): Work condition classification
        sede (SedeEnum): Location/sede of work
        days (List[DayEnum]): Working days
        professor_or_therapist_id (int): Foreign key to employee as professor/therapist
        conductor_id (int): Foreign key to employee as conductor
        track_assistant_id (int): Foreign key to employee as track assistant
        horse_id (int): Foreign key to assigned horse
        horse (Horse): Relationship to assigned horse
        inserted_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
        professor_or_therapist (Employee): Relationship to professor/therapist
        conductor (Employee): Relationship to conductor
        track_assistant (Employee): Relationship to track assistant
        jockey_amazon_id (int): Foreign key to JockeyAmazon
        jockey_amazon (JockeyAmazon): Relationship to associated jockey/amazon
    """

    __tablename__ = 'work_assignments'

    id = db.Column(db.Integer, primary_key=True)
    proposal = db.Column(SQLAEnum(WorkProposalEnum), nullable=False)
    condition = db.Column(SQLAEnum(WorkConditionEnum), nullable=False)
    sede = db.Column(SQLAEnum(SedeEnum), nullable=False)
    days = db.Column(db.ARRAY(SQLAEnum(DayEnum)), nullable=False)

    professor_or_therapist_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    conductor_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    track_assistant_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)

    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'), nullable=True)
    horse = db.relationship('Horse', back_populates='work_assignments')

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    professor_or_therapist = db.relationship('Employee', foreign_keys=[professor_or_therapist_id],
                                             backref='work_assignments_as_professor_or_therapist')
    conductor = db.relationship('Employee', foreign_keys=[conductor_id], backref='work_assignments_as_conductor')
    track_assistant = db.relationship('Employee', foreign_keys=[track_assistant_id],
                                      backref='work_assignments_as_track_assistant')
    jockey_amazon_id = db.Column(db.Integer, db.ForeignKey('jockeys_amazons.id', ondelete='CASCADE'), nullable=False)
    jockey_amazon = db.relationship('JockeyAmazon',
                                    back_populates='work_assignment',
                                    uselist=False)


class JockeyAmazon(db.Model, AddressMixin, PhoneMixin, EmergencyContactMixin):
    """
    Primary model for jockey/amazon information.

    This model stores comprehensive information about a jockey/amazon, including
    personal details, health information, educational status, family relationships,
    and work assignments. It inherits from multiple mixins for common fields.

    Attributes:
        id (int): Primary key
        first_name (str): First name, max length 100
        last_name (str): Last name, max length 100
        dni (str): Unique national ID number, max length 20
        birth_date (date): Date of birth
        birthplace (str): Place of birth, max length 100
        has_debts (bool): Debt status flag, defaults to False

        # Scholarship Information
        has_scholarship (bool): Scholarship status flag, defaults to False
        scholarship_observations (str): Notes about scholarship
        scholarship_percentage (float): Scholarship percentage if applicable

        # Disability Information
        has_disability (bool): Disability status flag, defaults to False
        disability_diagnosis (DisabilityDiagnosisEnum): Type of disability diagnosis
        disability_other (str): Additional disability information, max length 100
        disability_type (DisabilityTypeEnum): Classification of disability

        # Family and Benefits Information
        has_family_assignment (bool): Family assignment status flag
        family_assignment_type (FamilyAssignmentEnum): Type of family assignment
        has_pension (bool): Pension status flag
        pension_type (PensionEnum): Type of pension
        pension_details (str): Additional pension information

        # Social Security and Legal Information
        social_security (str): Social security details, max length 100
        social_security_number (str): Social security number, max length 50
        has_curatorship (bool): Curatorship status flag
        curatorship_observations (str): Notes about curatorship

        # Educational Information
        school_institution (SchoolInstitution): Related school information
        current_grade_year (str): Current grade/year in school, max length 50
        school_observations (str): Notes about schooling
        professionals (str): Related professional information

        # Relationships
        family_members (List[FamilyMember]): Related family members
        work_assignment (WorkAssignment): Related work assignment
        charges (List[Charge]): Related charges
        files (List[JockeyAmazonFile]): Related files

        # Timestamps and Status
        inserted_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
        is_deleted (bool): Deletion status flag, defaults to False

    Note:
        This model inherits from AddressMixin, PhoneMixin, and EmergencyContactMixin
        which provide additional fields for address, phone, and emergency contact information.
    """

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
    disability_type = db.Column(db.Enum(DisabilityTypeEnum), nullable=True)

    has_family_assignment = db.Column(db.Boolean, default=False)
    family_assignment_type = db.Column(db.Enum(FamilyAssignmentEnum), nullable=True)

    has_pension = db.Column(db.Boolean, default=False)
    pension_type = db.Column(db.Enum(PensionEnum), nullable=True)
    pension_details = db.Column(db.String(100), nullable=True)

    social_security = db.Column(db.String(100), nullable=True)
    social_security_number = db.Column(db.String(50), nullable=True)
    has_curatorship = db.Column(db.Boolean, default=False)
    curatorship_observations = db.Column(db.Text, nullable=True)

    school_institution = db.relationship('SchoolInstitution',
                                         cascade="all, delete-orphan",
                                         single_parent=True,
                                         passive_deletes=True,
                                         uselist=False)

    current_grade_year = db.Column(db.String(50), nullable=True)
    school_observations = db.Column(db.Text, nullable=True)

    professionals = db.Column(db.Text, nullable=True)

    family_members = db.relationship('FamilyMember',
                                     cascade="all, delete-orphan",
                                     single_parent=True,
                                     passive_deletes=True)

    work_assignment = db.relationship('WorkAssignment',
                                      cascade="all, delete-orphan",
                                      single_parent=True,
                                      passive_deletes=True,
                                      uselist=False)

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    family_member_jockey_amazon = db.Table('family_member_jockey_amazon',
                                           db.Column('family_member_id', db.Integer, db.ForeignKey('family_members.id'),
                                                     primary_key=True),
                                           db.Column('jockey_amazon_id', db.Integer,
                                                     db.ForeignKey('jockeys_amazons.id'), primary_key=True)
                                           )
    charges = db.relationship("Charge", back_populates="jya", lazy="select")
    files = db.relationship("JockeyAmazonFile",
                            back_populates="owner",
                            cascade="all, delete-orphan")

    is_deleted = db.Column(db.Boolean, nullable=False, default=False)


class JockeyAmazonFile(File):
    """
    File attachment model for jockey/amazon documents.

    This model extends the base File model to store files specifically related
    to jockeys/amazons, such as documentation, forms, or other attachments.

    Attributes:
        jockey_amazon_id (int): Foreign key to associated JockeyAmazon
        owner (JockeyAmazon): Relationship to owning jockey/amazon

    Note:
        Inherits all attributes from the base File model with a
        polymorphic identity of "jockey_amazon".
    """

    __mapper_args__ = {
        "polymorphic_identity": "jockey_amazon",
    }

    jockey_amazon_id = db.Column(db.Integer, db.ForeignKey("jockeys_amazons.id", ondelete='CASCADE'))
    owner = db.relationship("JockeyAmazon", back_populates="files")
