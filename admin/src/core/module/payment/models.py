from datetime import datetime
from src.core.database import db
from src.core.module.payment.data import PaymentTypeEnum
from src.core.module.employee.models import Employee


class Payment(db.Model):
    """
     Model representing a payment

    Attributes:
        id (int): The unique identifier of the payment.
        amount (float): The amount to be paid.
        payment_date (datetime.date): The date of the payment.
        payment_type (PaymentTypeEnum): The type of payment.
        description (str): The description of the payment.
        beneficiary_id (int): The ID of the beneficiary.
        beneficiary (Employee): The beneficiary of the payment.
        is_archived (bool): Indicates if the payment is deleted.
        inserted_at (datetime.datetime): The timestamp when the payment was inserted.
        updated_at (datetime.datetime): The timestamp when the payment was last updated.
    """
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=datetime.today)
    payment_type = db.Column(db.Enum(PaymentTypeEnum), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # Optional relationship to Employee
    beneficiary_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=True)
    beneficiary = db.relationship("Employee", backref=db.backref("payments", lazy=True))
    
    is_archived = db.Column(db.Boolean, default=False, nullable=False) 
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)