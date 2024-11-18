from abc import abstractmethod
from typing import List, Dict
from datetime import datetime

from src.core.database import db as database
from src.core.module.publication.models import Publication, EstadoPublicacionEnum
from src.core.module.common.repositories import apply_filters
from .mappers import PublicationMapper as Mapper


class AbstractPublicationRepository:
    """
    Abstract base class for publication repositories.

    This class defines the interface for publication repositories, including methods
    for adding, retrieving, updating, and managing publication states.
    """

    @abstractmethod
    def add_publication(self, publication: Publication) -> Dict:
        """
        Add a new publication to the repository.

        Args:
            publication (Publication): The publication to add.

        Returns:
            Dict: The added publication as a dictionary.
        """
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
        Retrieve a paginated list of publications.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of publications per page.
            search_query (Dict, optional): The search query to filter publications.
            order_by (list, optional): The order by criteria.

        Returns:
            A paginated list of publications.
        """
        pass

    @abstractmethod
    def get_by_id(self, publication_id: int) -> Dict | None:
        """
        Retrieve a publication by its ID.

        Args:
            publication_id (int): The ID of the publication to retrieve.

        Returns:
            Dict | None: The publication data as a dictionary, or None if not found.
        """
        pass

    @abstractmethod
    def update_publication(self, publication_id: int, data: Dict) -> bool:
        """
        Update a publication's information.

        Args:
            publication_id (int): The ID of the publication to update.
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
    def logical_delete_publication(self, publication_id: int) -> bool:
        """
        Logically delete a publication.

        Args:
            publication_id (int): The ID of the publication to logically delete.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def recover_publication(self, publication_id: int) -> bool:
        """
        Recover a logically deleted publication.

        Args:
            publication_id (int): The ID of the publication to recover.

        Returns:
            bool: True if recovered successfully, False otherwise.
        """
        pass


class PublicationRepository(AbstractPublicationRepository):
    """
    Concrete implementation of the AbstractPublicationRepository.

    This class provides methods for adding, retrieving, updating, and managing
    publications in the database.
    """

    def __init__(self):
        """
        Initialize the PublicationRepository.
        """
        self.db = database

    def add_publication(self, publication: Publication) -> Dict:
        """
        Add a new publication to the repository.

        Args:
            publication (Publication): The publication to add.

        Returns:
            Dict: The added publication as a dictionary.
        """
        self.db.session.add(publication)
        self.db.session.flush()
        self.save()
        return Mapper.from_entity(publication)

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

        query = Publication.query

        # Handle date range filters
        if search_query and "filters" in search_query and search_query["filters"]:
            if "start_date" in search_query["filters"]:
                query = (query
                         .filter(Publication.publish_date > search_query["filters"]["start_date"]))
                search_query["filters"].pop("start_date")

            if "end_date" in search_query["filters"]:
                query = (query
                         .filter(Publication.publish_date < search_query["filters"]["end_date"]))
                search_query["filters"].pop("end_date")

        query = apply_filters(Publication, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def __get_by_id(self, publication_id: int) -> Publication:
        """
        Internal method to retrieve a publication by its ID.

        Args:
            publication_id (int): The ID of the publication to retrieve.

        Returns:
            Publication: The publication entity.
        """
        return Publication.query.get(publication_id)

    def get_by_id(self, publication_id: int) -> Dict | None:
        """
        Retrieve a publication by its ID.

        Args:
            publication_id (int): The ID of the publication to retrieve.

        Returns:
            Dict | None: The publication data as a dictionary, or None if not found.
        """
        publication = self.db.session.query(Publication).filter(Publication.id == publication_id).first()
        return Mapper.from_entity(publication) if publication else None

    def update_publication(self, publication_id: int, data: Dict) -> bool:
        """
        Update a publication's information.

        Args:
            publication_id (int): The ID of the publication to update.
            data (Dict): The updated publication data.

        Returns:
            bool: True if updated successfully, False otherwise.
        """
        publication = Publication.query.filter_by(id=publication_id)
        if not publication:
            return False
        publication.update(data)
        self.save()
        return True

    def delete_publication(self, publication_id: int) -> bool:
        """
        Delete a publication.

        Args:
            publication_id (int): The ID of the publication to delete.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        publication = self.__get_by_id(publication_id)
        if not publication:
            return False
        self.db.session.delete(publication)
        self.save()
        return True

    def logical_delete_publication(self, publication_id: int) -> bool:
        """
        Logically delete a publication.

        Args:
            publication_id (int): The ID of the publication to logically delete.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        publication = Publication.query.get(publication_id)
        if not publication or publication.is_deleted:
            return False
        publication.is_deleted = True
        publication.status = EstadoPublicacionEnum.ARCHIVED
        publication.update_date = datetime.now()
        self.save()
        return True

    def recover_publication(self, publication_id: int) -> bool:
        """
        Recover a logically deleted publication.

        Args:
            publication_id (int): The ID of the publication to recover.

        Returns:
            bool: True if recovered successfully, False otherwise.
        """
        publication = Publication.query.get(publication_id)
        if not publication or not publication.is_deleted:
            return False
        publication.is_deleted = False
        publication.status = EstadoPublicacionEnum.DRAFT
        publication.update_date = datetime.now()
        self.save()
        return True

    def save(self):
        """
        Commit the current transaction to the database.

        Returns:
            None
        """
        self.db.session.commit()
