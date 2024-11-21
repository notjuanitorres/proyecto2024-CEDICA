from abc import abstractmethod
from typing import List, Dict
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
            data (Dict): The updated publication data.

        Returns:
            bool: True if updated successfully, False otherwise.
        """
        pass

    @abstractmethod
    def delete_publication(self, publication_id: int) -> bool:
        """
        Delete a publication.

        Args:
            publication_id (int): The ID of the publication to delete.

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
        Add a new publication to the repository.

        Args:
            publication (Publication): The publication to add.

        Returns:
            Dict: The added publication as a dictionary.
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
        Retrieve a paginated list of publications.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of publications per page.
            search_query (Dict, optional): The search query to filter publications.
            order_by (List, optional): The order by criteria.

        Returns:
            A paginated list of publications.
        """
        max_per_page = 100

        query = Message.query

        # Handle date range and state filters
        if search_query and "filters" in search_query and search_query["filters"]:
            pass

        query = apply_filters(Message, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def __get_by_id(self, message_id: int) -> Message:
        """
        Internal method to retrieve a publication by its ID.

        Args:
            publication_id (int): The ID of the publication to retrieve.

        Returns:
            Publication: The publication entity.
        """
        return Message.query.get(message_id)

    def get_by_id(self, message_id: int) -> Dict | None:
        """
        Retrieve a publication by its ID.

        Args:
            message_id (int): The ID of the message to retrieve.

        Returns:
            Dict | None: The publication data as a dictionary, or None if not found.
        """
        message = self.db.session.query(Message).filter(message.id == message_id).first()
        return Mapper.from_entity(message) if message else None
