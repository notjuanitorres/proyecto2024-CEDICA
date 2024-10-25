from typing import Dict
from src.core.module.payment.models import Payment
from src.core.module.employee.models import Employee


class PaymentMapper:
    """
    A mapper class for converting between Payment entities and dictionaries.

    Methods:
        to_entity(data: Dict) -> Payment:
            Converts a dictionary of payment data to a Payment entity.

        from_entity(payment: Payment) -> Dict:
            Converts a Payment entity to a dictionary of payment data.
    """
    @staticmethod
    def to_entity(data: Dict) -> Payment:
        """
        Converts a dictionary of payment data to a Payment entity.

        Args:
            data (Dict): A dictionary containing payment details, including "amount",
                         "payment_date", "payment_type", "description", and "beneficiary_id".

        Returns:
            Payment: An instance of the Payment entity with the provided data.
        """
        return Payment(
            amount=data.get("amount"),
            payment_date=data.get("payment_date"),
            payment_type=data.get("payment_type"),
            description=data.get("description"),
            beneficiary_id=data.get("beneficiary_id"),
            is_archived=data.get("is_archived", False),
        )

    @staticmethod
    def from_entity(payment: Payment) -> Dict:
        """
        Converts a Payment entity to a dictionary of payment data.

        Args:
            payment (Payment): An instance of the Payment entity.

        Returns:
            Dict: A dictionary containing the payment's attributes, including "id",
                  "amount", "payment_date", "payment_type", "description", "beneficiary_id",
                  "inserted_at", and "updated_at".
        """
        return {
            "id": payment.id,
            "amount": str(payment.amount),  # Convertir a string para evitar problemas de serialización
            "payment_date": payment.payment_date,
            "payment_type": payment.payment_type.name,
            "description": payment.description,
            "beneficiary_id": payment.beneficiary_id,
            "inserted_at": payment.inserted_at,
            "updated_at": payment.updated_at,
            "is_archived": payment.is_archived
        }
