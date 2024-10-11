from src.core.database import db
from datetime import datetime

from enum import Enum as pyEnum


class PaymentMethod(pyEnum):
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
    payment_method = db.Column(db.Enum(PaymentMethod), nullable=False)
    observations = db.Column(db.String(255), nullable=True)

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    # employee = db.relationship("Employee", backref=db.backref("charges", lazy="dynamic"))

    # TODO: uncomment when JYA model is created
    # jya_id = db.Column(db.Integer, db.ForeignKey("jyas.id"), nullable=True)
    # jya = db.relationship("JYA", backref=db.backref("charge"), uselist=False)
