from typing import Dict
from src.core.module.contact.models import Message, MessageStateEnum

class ContactMapper:
    """
    A mapper class for converting between Message entities and data transfer objects (DTOs).
    """

    @classmethod
    def from_entity(cls, message: Message) -> Dict:
        """
        Convert a Message entity to a dictionary.

        Args:
            message (Message): The Message entity to convert.

        Returns:
            Dict: A dictionary representation of the Message entity.
        """
        return {
            "id": message.id,
            "name": message.name,
            "email": message.email,
            "message": message.message,
            "status": message.status,
            "inserted_at": message.inserted_at,
            "updated_at": message.updated_at,
            "is_deleted": message.is_deleted,
        }

    @classmethod
    def to_entity(cls, data: Dict) -> Message:
        """
        Convert a dictionary to a Message entity.

        Args:
            data (Dict): The dictionary containing message data.

        Returns:
            Message: The Message entity created from the provided data.
        """
        print(data)
            
        message = Message(
            name=data.get("name"),
            email=data.get("email"),
            message=data.get("message"),
            status=data.get("status", MessageStateEnum.PENDING),
        )

        print(message)

        return message

    @classmethod
    def from_create_form(cls, data: Dict) -> Dict:
        """
        Convert form data to a dictionary suitable for creating a Message entity.

        Args:
            data (Dict): The form data.

        Returns:
            Dict: A dictionary representation of the form data.
        """
        return {
            "name": data.get("name"),
            "email": data.get("email"),
            "message": data.get("message"),
            "status": data.get("status", MessageStateEnum.PENDING),
        }

    @classmethod
    def from_edit_form(cls, data: Dict) -> Dict:
        """
        Convert form data to a dictionary suitable for updating a Message entity.

        Args:
            data (Dict): The form data.

        Returns:
            Dict: A dictionary representation of the form data.
        """
        return {
            "name": data.get("name"),
            "email": data.get("email"),
            "message": data.get("message"),
            "status": data.get("status"),
        }

    @classmethod
    def to_form(cls, data: Dict) -> Dict:
        """
        Convert a dictionary to a form data representation.

        Args:
            data (Dict): The dictionary containing message data.

        Returns:
            Dict: A dictionary representation of the message data suitable for form population.
        """
        return {
            "name": data.get("name"),
            "email": data.get("email"),
            "message": data.get("message"),
            "status": data.get("status"),
        }