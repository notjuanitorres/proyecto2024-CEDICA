from typing import Dict
from src.core.module.publication.models import Publication, EstadoPublicacionEnum


class PublicationMapper:
    """
    A mapper class for converting between Publication entities and data transfer objects (DTOs).
    """

    @classmethod
    def from_entity(cls, publication: Publication) -> Dict:
        """
        Convert a Publication entity to a dictionary.

        Args:
            publication (Publication): The Publication entity to convert.

        Returns:
            Dict: A dictionary representation of the Publication entity.
        """
        return {
            "id": publication.id,
            "publish_date": publication.publish_date,
            "create_date": publication.create_date,
            "update_date": publication.update_date,
            "title": publication.title,
            "summary": publication.summary,
            "content": publication.content,
            "author_id": publication.author_id,
            "status": publication.status.value,
            "type": publication.type.value,
            "is_deleted": publication.is_deleted,
        }

    @classmethod
    def to_entity(cls, data: Dict) -> Publication:
        """
        Convert a dictionary to a Publication entity.

        Args:
            data (Dict): The dictionary containing publication data.

        Returns:
            Publication: The Publication entity created from the provided data.
        """
        return Publication(
            title=data.get("title"),
            summary=data.get("summary"),
            content=data.get("content"),
            author_id=data.get("author_id"),
            status=data.get("status", EstadoPublicacionEnum.DRAFT),
            publish_date=data.get("publish_date"),
            type=data.get("type"),
        )

    @classmethod
    def from_create_form(cls, data: Dict) -> Dict:
        """
        Convert form data to a dictionary suitable for creating a Publication entity.

        Args:
            data (Dict): The form data.

        Returns:
            Dict: A dictionary representation of the form data.
        """
        return {
            "title": data.get("title"),
            "summary": data.get("summary"),
            "content": data.get("content"),
            "status": data.get("status"),
            "author_id": None,  # Author ID is not provided in the form, but it should be given in the controller.
            "type": data.get("type"),
        }

    @classmethod
    def from_edit_form(cls, data: Dict) -> Dict:
        """
        Convert form data to a dictionary suitable for updating a Publication entity.

        Args:
            data (Dict): The form data.

        Returns:
            Dict: A dictionary representation of the form data.
        """
        return {
            "title": data.get("title"),
            "summary": data.get("summary"),
            "content": data.get("content"),
            "status": data.get("status"),
            "type": data.get("type"),
        }

    @classmethod
    def to_form(cls, data: Dict) -> Dict:
        """
        Convert a dictionary to a form data representation.

        Args:
            data (Dict): The dictionary containing publication data.

        Returns:
            Dict: A dictionary representation of the publication data suitable for form population.
        """
        return {
            "title": data.get("title"),
            "summary": data.get("summary"),
            "content": data.get("content"),
            "status": data.get("status"),
            "author_id": data.get("author_id"),
            "type": data.get("type"),
        }
