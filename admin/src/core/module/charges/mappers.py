from typing import Dict
from src.core.module.charges.models import Charge


class ChargeMapper:
    @classmethod
    def from_entity(cls, charge: Charge) -> Dict:
        return {
            "id": charge.id,
            "amount": charge.amount,
            "observations": charge.observations,
            "payment_method": charge.payment_method.value,
            "date_of_charge": charge.date_of_charge,
            "employee_id": charge.employee_id,
            "jya_id": charge.jya_id,
            "inserted_at": charge.inserted_at,
            "updated_at": charge.updated_at,
            "is_archived": charge.is_archived,
        }

    @classmethod
    def to_entity(cls, data: Dict) -> "Charge":
        return Charge(
            amount=data.get("amount"),
            observations=data.get("observations"),
            payment_method=data.get("payment_method"),
            date_of_charge=data.get("date_of_charge"),
            employee_id=data.get("employee_id"),
            jya_id=data.get("jya_id"),
            is_archived=data.get("is_archived"),
        )

    @classmethod
    def from_form(cls, data: Dict) -> Dict:
        return {
            "amount": data.get("amount"),
            "observations": data.get("observations"),
            "payment_method": data.get("payment_method"),
            "date_of_charge": data.get("date_of_charge"),
            # "employee_id": data.get("employee_id"),
            # "jya_id": data.get("jya_id"),
        }

    @classmethod
    def to_form(cls, data: Dict) -> Dict:
        return {
            "amount": data.get("amount"),
            "observations": data.get("observations"),
            "payment_method": data.get("payment_method"),
            "date_of_charge": data.get("date_of_charge"),
            # "employee_id": data.get("employee_id"),
            # "jya_id": data.get("jya_id"),
        }

    @classmethod
    def from_session(cls, data: Dict):
        return {
            "amount": data.get("amount"),
            "observations": data.get("observations"),
            "payment_method": data.get("payment_method"),
            "date_of_charge": data.get("date_of_charge"),
            "employee_id": data.get("employee_id"),
            "jya_id": data.get("jya_id"),
        }

    @classmethod
    def to_session(cls, data: Dict):
        return {
            "amount": data.get("amount"),
            "observations": data.get("observations"),
            "payment_method": data.get("payment_method"),
            "date_of_charge": data.get("date_of_charge"),
            "employee_id": data.get("employee_id"),
            "jya_id": data.get("jya_id"),
        }
