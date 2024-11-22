from abc import abstractmethod
from typing import List, Dict, Optional
from datetime import datetime

from src.core.database import db as database
from src.core.module.contact.models import Message, MessageStateEnum
from src.core.module.common.repositories import apply_filters, apply_search_criteria
from .mappers import ContactMapper as Mapper

class AbstractContactRepository:
    @abstractmethod
    def add_message(self, message: Message) -> Dict:
        pass

    @abstractmethod
    def get_page(
            self,
            page: int,
            per_page: int,
            search_query: Dict = None,
            order_by: list = None,
    ):
        """
        Retrieve a paginated list of messages.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of messages per page.
            search_query (Dict, optional): The search query to filter messages.
            order_by (list, optional): The order by criteria.

        Returns:
            A paginated list of messages.
        """
        pass

    @abstractmethod
    def update_message(self, message_id: int, data: Dict) -> bool:
        """
        Update a message's information.

        Args:
            message_id (int): The ID of the message to update.
            data (Dict): The updated message data.

        Returns:
            bool: True if updated successfully, False otherwise.
        """
        pass

    @abstractmethod
    def delete_message(self, message_id: int) -> bool:
        """
        Delete a message.

        Args:
            message_id (int): The ID of the message to delete.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def logical_delete_message(self, message_id: int) -> bool:
        """
        Logically delete a message.

        Args:
            message_id (int): The ID of the message to logically delete.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def recover_message(self, message_id: int) -> bool:
        """
        Recover a logically deleted message.

        Args:
            message_id (int): The ID of the message to recover.

        Returns:
            bool: True if recovered successfully, False otherwise.
        """
        pass


class ContactRepository(AbstractContactRepository):
    """
    """

    def __init__(self):
        """
        Initialize the ContactRepository.
        """
        self.db = database
    
    def save(self):
        """Commit current transaction to the database."""
        self.db.session.commit()

    def add_message(self, message: Message) -> Dict:
        """
        Add a new message to the repository.

        Args:
            message (message): The message to add.

        Returns:
            Dict: The added message as a dictionary.
        """
        self.db.session.add(message)
        self.db.session.flush()
        self.save()

        return Mapper.from_entity(message)

    def get_page(
            self,
            page: int,
            per_page: int,
            search_query: Dict = None,
            order_by: List = None,
    ):
        """
        Retrieve a paginated list of messages.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of messages per page.
            search_query (Dict, optional): The search query to filter messages.
            order_by (List, optional): The order by criteria.

        Returns:
            A paginated list of messages.
        """
        max_per_page = 100

        query = Message.query

        # Handle date range and state filters
        if search_query and "filters" in search_query:
            filters = search_query["filters"]

        if "status" in filters and not filters["status"]:
                del filters["status"]

        search_query["filters"] = filters

        query = apply_filters(Message, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def __get_by_id(self, message_id: int) -> Message:
        """
        Internal method to retrieve a message by its ID.

        Args:
            message_id (int): The ID of the message to retrieve.

        Returns:
            message: The message entity.
        """
        return Message.query.get(message_id)

    def get_by_id(self, message_id: int) -> Optional[Message]:
        """
        Retrieve a message by its ID.

        Args:
            message_id (int): The ID of the message to retrieve.

        Returns:
            Dict | None: The message data as a dictionary, or None if not found.
        """
        message = self.db.session.query(Message).filter(Message.id == message_id).first()
        return message
    
    def logical_delete_message(self, message_id: int) -> bool:
        """
        Logically delete a message.

        Args:
            message_id (int): The ID of the message to logically delete.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        message = self.get_by_id(message_id)
        if not message or message.is_deleted:
            return False
        message.is_deleted = True
        self.save()
        return True

    def recover(self, message_id: int) -> bool:
        """
        Recover an archived `Message` entity by setting its `is_deleted` flag to False.

        Args:
            message_id (int): The ID of the message to recover.

        Returns:
            bool: True if the message was successfully recovered, False otherwise.
        """
        message = self.get_by_id(message_id)
        if not message or not message.is_deleted:
            return False
        message.is_deleted = False
        self.save()
        return True
    

    def delete(self, message_id: int) -> bool:
        """
        Permanently delete a `Message` entity.

        Args:
            message_id (int): The ID of the message to delete.

        Returns:
            bool: True if the message was successfully deleted, False otherwise.
        """
        message = Message.query.filter_by(id=message_id)
        if not message:
            return False
        message.delete()
        self.save()
        return True
