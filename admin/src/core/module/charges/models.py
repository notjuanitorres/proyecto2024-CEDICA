from src.core.database import db
from datetime import datetime
from enum import Enum as pyEnum
from src.core.module.jockey_amazon.models import JockeyAmazon
# TODO: uncomment when JYA model is imported somewhere else
# https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models


class PaymentMethodEnum(pyEnum):
    """
    Enumeration for different payment methods.

    Attributes:
        CASH (str): Cash payment method.
        CREDIT_CARD (str): Credit card payment method.
        DEBIT_CARD (str): Debit card payment method.
        WIRE_TRANSFER (str): Wire transfer payment method.
        CHECK (str): Check payment method.
        OTHER (str): Other payment method.
    """
    CASH = "Efectivo"
    CREDIT_CARD = "Tarjeta de crédito"
    DEBIT_CARD = "Tarjeta de débito"
    WIRE_TRANSFER = "Transferencia bancaria"
    CHECK = "Cheque"
    OTHER = "Otro"


class Charge(db.Model):
    """
    Represents a charge in the system.

    Attributes:
        id (int): The unique identifier for the charge.
        date_of_charge (datetime.date): The date when the charge was made.
        amount (float): The amount of the charge.
        payment_method (PaymentMethodEnum): The payment method used for the charge.
        observations (str): Additional observations about the charge.
        is_archived (bool): Indicates whether the charge is archived.
        inserted_at (datetime): The timestamp when the charge was created.
        updated_at (datetime): The timestamp when the charge was last updated.
        employee_id (int): The ID of the employee associated with the charge.
        employee (Employee): The employee associated with the charge.
        jya_id (int): The ID of the jockey or amazon associated with the charge.
        jya (JockeyAmazon): The jockey or amazon associated with the charge.
    """

    __tablename__ = "charges"

    id = db.Column(db.Integer, primary_key=True)
    date_of_charge = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Enum(PaymentMethodEnum), nullable=False)
    observations = db.Column(db.String(255), nullable=True)

    is_archived = db.Column(db.Boolean, default=False, nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    employee = db.relationship("Employee", back_populates="charges", lazy="select")

    jya_id = db.Column(db.Integer, db.ForeignKey("jockeys_amazons.id"), nullable=False)
    jya = db.relationship("JockeyAmazon", back_populates="charges", uselist=False)