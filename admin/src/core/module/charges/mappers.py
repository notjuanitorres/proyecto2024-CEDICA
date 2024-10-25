from typing import Dict
from src.core.module.charges.models import Charge


class ChargeMapper:
    """
    A mapper class for converting between Charge entities and data transfer objects (DTOs).
    """

    @classmethod
    def from_entity(cls, charge: Charge) -> Dict:
        """
        Convert a Charge entity to a dictionary.

        Args:
            charge (Charge): The Charge entity to convert.

        Returns:
            Dict: A dictionary representation of the Charge entity.
        """
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
    def to_entity(cls, data: Dict) -> Charge:
        """
        Convert a dictionary to a Charge entity.

        Args:
            data (Dict): The dictionary containing charge data.

        Returns:
            Charge: The Charge entity created from the provided data.
        """
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
        """
        Convert form data to a dictionary suitable for creating or updating a Charge entity.

        Args:
            data (Dict): The form data.

        Returns:
            Dict: A dictionary representation of the form data.
        """
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
        """
        Convert a dictionary to a form data representation.

        Args:
            data (Dict): The dictionary containing charge data.

        Returns:
            Dict: A dictionary representation of the charge data suitable for form population.
        """
        return {
            "amount": data.get("amount"),
            "observations": data.get("observations"),
            "payment_method": data.get("payment_method"),
            "date_of_charge": data.get("date_of_charge"),
            # "employee_id": data.get("employee_id"),
            # "jya_id": data.get("jya_id"),
        }

    @classmethod
    def from_session(cls, data: Dict) -> Dict:
        """
        Convert session data to a dictionary suitable for creating or updating a Charge entity.

        Args:
            data (Dict): The session data.

        Returns:
            Dict: A dictionary representation of the session data.
        """
        return {
            "amount": data.get("amount"),
            "observations": data.get("observations"),
            "payment_method": data.get("payment_method"),
            "date_of_charge": data.get("date_of_charge"),
            "employee_id": data.get("employee_id"),
            "jya_id": data.get("jya_id"),
        }

    @classmethod
    def to_session(cls, data: Dict) -> Dict:
        """
        Convert a dictionary to a session data representation.

        Args:
            data (Dict): The dictionary containing charge data.

        Returns:
            Dict: A dictionary representation of the charge data suitable for session storage.
        """
        return {
            "amount": data.get("amount"),
            "observations": data.get("observations"),
            "payment_method": data.get("payment_method"),
            "date_of_charge": data.get("date_of_charge"),
            "employee_id": data.get("employee_id"),
            "jya_id": data.get("jya_id"),
        }