from typing import Dict, List
from .models import Horse, HorseFile


class HorseMapper:
    """
    Mapper class for converting between Horse entities and dictionaries.
    """

    @classmethod
    def create_file(cls, document_type, file_information):
        """
        Create a HorseFile instance from file information.

        Args:
            document_type (str): The type of the document.
            file_information (dict): The information of the file.

        Returns:
            HorseFile: The created HorseFile instance.
        """
        horse_file = HorseFile(
            path=file_information.get("path"),
            title=file_information.get("title"),
            is_link=file_information.get("is_link"),
            filetype=file_information.get("filetype"),
            filesize=file_information.get("filesize"),
            tag=document_type,
        )
        return horse_file

    @classmethod
    def create_files(cls, files):
        """
        Create a list of HorseFile instances from a list of file information.

        Args:
            files (list): A list of tuples containing document type and file information.

        Returns:
            list: A list of created HorseFile instances.
        """
        created_files = []
        for doc_type, files_info in files:
            for file_info in files_info:
                if file_info:
                    created_files.append(cls.create_file(doc_type, file_info))
        return created_files

    @classmethod
    def to_entity(cls, data: Dict, files: List) -> Horse:
        """
        Convert a dictionary to a Horse entity.

        Args:
            data (dict): The data dictionary.
            files (list): A list of file information.

        Returns:
            Horse: The created Horse entity.
        """
        horse = Horse(
            name=data.get("name"),
            birth_date=data.get("birth_date"),
            sex=data.get("sex"),
            breed=data.get("breed"),
            coat=data.get("coat"),
            is_donation=data.get("is_donation"),
            admission_date=data.get("admission_date"),
            assigned_facility=data.get("assigned_facility"),
            ja_type=data.get("ja_type"),
        )

        if files:
            horse_files = cls.create_files(files)
            for file in horse_files:
                if file:
                    horse.files.append(file)

        return horse

    @classmethod
    def from_entity(cls, horse: Horse, documents: bool = True) -> Dict:
        """
        Convert a Horse entity to a dictionary.

        Args:
            horse (Horse): The Horse entity.
            documents (bool): Whether to include documents.

        Returns:
            dict: The serialized horse data.
        """
        serialized_horse = {
            "id": horse.id,
            "name": horse.name,
            "birth_date": horse.birth_date,
            "sex": horse.sex,
            "breed": horse.breed,
            "coat": horse.coat,
            "is_donation": horse.is_donation,
            "admission_date": horse.admission_date,
            "assigned_facility": horse.assigned_facility,
            "ja_type": horse.ja_type.value,
            "inserted_at": horse.inserted_at,
            "updated_at": horse.updated_at,
            "is_deleted": horse.is_deleted
        }

        if documents:
            serialized_horse["files"] = [file.to_dict() for file in horse.files if file]

        return serialized_horse

    @classmethod
    def from_simple_form(cls, data: Dict):
        """
        Convert a simple form dictionary to a horse data dictionary.

        Args:
            data (dict): The form data dictionary.

        Returns:
            dict: The horse data dictionary.
        """
        return {
            "name": data.get("name"),
            "birth_date": data.get("birth_date"),
            "sex": data.get("sex"),
            "breed": data.get("breed"),
            "coat": data.get("coat"),
            "is_donation": data.get("is_donation"),
            "admission_date": data.get("admission_date"),
            "assigned_facility": data.get("assigned_facility"),
            "ja_type": data.get("ja_type"),
            "is_deleted": data.get("is_deleted", False),
        }
