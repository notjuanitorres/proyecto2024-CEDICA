from src.core.database import db
from datetime import datetime

from enum import Enum as pyEnum

from src.core.module.jockey_amazon.models import JockeyAmazon
# TODO: uncomment when JYA model is imported somewhere else
# https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models


class PaymentMethodEnum(pyEnum):
    CASH = "Efectivo"
    CREDIT_CARD = "Tarjeta de crédito"
    DEBIT_CARD = "Tarjeta de débito"
    WIRE_TRANSFER = "Transferencia bancaria"
    CHECK = "Cheque"
    OTHER = "Otro"


class Charge(db.Model):
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

    # TODO: uncomment when JYA model is created
    jya_id = db.Column(db.Integer, db.ForeignKey("jockeys_amazons.id"), nullable=False)
    jya = db.relationship("JockeyAmazon", back_populates="charges", uselist=False)
