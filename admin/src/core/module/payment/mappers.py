from typing import Dict
from src.core.module.payment.models import Payment
from src.core.module.employee.models import Employee

class PaymentMapper:
    @staticmethod
    def to_entity(data: Dict) -> Payment:
        return Payment(
            amount=data.get("amount"),
            payment_date=data.get("payment_date"),
            payment_type=data.get("payment_type"),
            description=data.get("description"),
            beneficiary_id=data.get("beneficiary_id"),
        )

    @staticmethod
    def from_entity(payment: Payment) -> Dict:
        return {
            "id": payment.id,
            "amount": str(payment.amount),  # Convertir a string para evitar problemas de serialización
            "payment_date": payment.payment_date,
            "payment_type": payment.payment_type.name,
            "description": payment.description,
            "beneficiary_id": payment.beneficiary_id,
            "beneficiary_name": payment.beneficiary.fullname if payment.beneficiary else None,
            "inserted_at": payment.inserted_at,
            "updated_at": payment.updated_at,
        }