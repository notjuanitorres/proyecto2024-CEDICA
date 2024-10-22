from abc import abstractmethod
from typing import List, Dict
from src.core.module.common.repositories import apply_filters, apply_multiple_search_criteria, apply_filter_criteria
from src.core.module.equestrian.models import Horse, HorseTrainers, HorseFile
from src.core.database import db as database
from src.core.module.employee.models import Employee
from src.core.module.equestrian.mappers import HorseMapper


class AbstractEquestrianRepository:
    """
    Abstract repository for equestrian operations.

    Attributes:
        storage_path (str): The path for storing equestrian data.
    """
    def __init__(self):
        self.storage_path = "equestrian/"

    @abstractmethod
    def add(self, horse: Horse) -> Dict:
        """
        Add a new horse to the repository.

        Args:
            horse (Horse): The horse to add.

        Returns:
            Dict: The added horse data.
        """
        pass

    @abstractmethod
    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int = 10,
            search_query: Dict = None,
            order_by: list = None,
    ):
        """
        Get a paginated list of horses.

        Args:
            page (int): The page number.
            per_page (int): The number of items per page.
            max_per_page (int): The maximum number of items per page.
            search_query (Dict): The search query parameters.
            order_by (list): The order by parameters.

        Returns:
            Pagination: The paginated list of horses.
        """
        pass

    @abstractmethod
    def get_by_id(self, horse_id: int, documents: bool = True) -> Dict | None:
        """
        Get a horse by its ID.

        Args:
            horse_id (int): The ID of the horse.
            documents (bool): Whether to include documents.

        Returns:
            Dict | None: The horse data or None if not found.
        """
        pass

    @abstractmethod
    def update(self, horse_id: int, data: Dict) -> bool:
        """
        Update a horse's data.

        Args:
            horse_id (int): The ID of the horse.
            data (Dict): The data to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        pass

    @abstractmethod
    def delete(self, horse_id: int) -> bool:
        """
        Delete a horse

        Args:
            horse_id (int): The ID of the horse.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_trainers_of_horse(self, horse_id: int) -> List:
        """
        Get the trainers of a horse.

        Args:
            horse_id (int): The ID of the horse.

        Returns:
            List: The list of trainers.
        """
        pass

    @abstractmethod
    def add_horse_trainers(self, horse_id: int, trainers_ids: List[int]):
        """
        Add trainers to a horse.

        Args:
            horse_id (int): The ID of the horse.
            trainers_ids (List[int]): The list of trainer IDs.
        """
        pass

    @abstractmethod
    def add_document(self, horse_id: int, document: HorseFile) -> None:
        """
        Add a document to a horse.

        Args:
            horse_id (int): The ID of the horse.
            document (HorseFile): The document to add.
        """
        raise NotImplementedError

    @abstractmethod
    def get_document(self, horse_id: int, document_id: int) -> HorseFile:
        """
        Get a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            document_id (int): The ID of the document.

        Returns:
            HorseFile: The document.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_document(self, horse_id: int, document_id: int) -> bool:
        """
        Delete a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            document_id (int): The ID of the document.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def update_document(self, horse_id: int, document_id: int, data: Dict) -> bool:
        """
        Update a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            document_id (int): The ID of the document.
            data (Dict): The data to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def get_file_page(
            self,
            horse_id: int,
            page: int,
            per_page: int,
            max_per_page: int = 10,
            search_query: Dict = None,
            order_by: List = None,
    ):
        """
        Get a paginated list of files for a horse.

        Args:
            horse_id (int): The ID of the horse.
            page (int): The page number.
            per_page (int): The number of items per page.
            max_per_page (int): The maximum number of items per page.
            search_query (Dict): The search query parameters.
            order_by (List): The order by parameters.

        Returns:
            Pagination: The paginated list of files.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_horse_trainer(self, horse_id: int, trainer_id: int) -> bool:
        """
        Remove a trainer from a horse.

        Args:
            horse_id (int): The ID of the horse.
            trainer_id (int): The ID of the trainer.

        Returns:
            bool: True if the removal was successful, False otherwise.
        """
        raise NotImplementedError

    
    @abstractmethod
    def get_active_horses(self, page: int = 1, search: str = "", activity: str = "") -> bool:
        """
        Get a paginated list with the active horses.

        Args:
            page (int): Page requested.
            search (str): A text for searching hose.
            activity (str): Filter by activities assigned to the horse.

        Returns:
            bool: True if the removal was successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def archive_horse(self, horse_id: int) -> bool:
        """
        Archive a horse.

        Args:
            horse_id (int): The ID of the horse.

        Returns:
            bool: True if the archiving was successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def recover_horse(self, horse_id: int) -> bool:
        """
        Recover an archived horse.

        Args:
            horse_id (int): The ID of the horse.

        Returns:
            bool: True if the recovery was successful, False otherwise.
        """
        raise NotImplementedError


class EquestrianRepository(AbstractEquestrianRepository):
    """
    Repository for equestrian operations.
    """
    def __init__(self):
        super().__init__()
        self.db = database

    def add(self, horse: Horse):
        """
        Add a new horse to the repository.

        Args:
            horse (Horse): The horse to add.

        Returns:
            Dict: The added horse data.
        """
        self.db.session.add(horse)
        self.db.session.flush()
        self.save()
        return HorseMapper.from_entity(horse)

    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int = 10,
            search_query: Dict = None,
            order_by: List = None,
    ):
        """
        Get a paginated list of horses.

        Args:
            page (int): The page number.
            per_page (int): The number of items per page.
            max_per_page (int): The maximum number of items per page.
            search_query (Dict): The search query parameters.
            order_by (List): The order by parameters.

        Returns:
            Pagination: The paginated list of horses.
        """
        query = Horse.query

        query = apply_filters(Horse, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, horse_id: int, documents: bool = True) -> Dict | None:
        """
        Get a horse by its ID.

        Args:
            horse_id (int): The ID of the horse.
            documents (bool): Whether to include documents.

        Returns:
            Dict | None: The horse data or None if not found.
        """
        horse = self.__get_by_id(horse_id)
        if not horse:
            return None
        return HorseMapper.from_entity(horse, documents=documents)

    def __get_by_id(self, horse_id: int) -> Horse:
        """
        Get a horse by its ID.

        Args:
            horse_id (int): The ID of the horse.

        Returns:
            Horse: The horse.
        """
        return self.db.session.query(Horse).filter(Horse.id == horse_id).first()

    def update(self, horse_id: int, data: Dict):
        """
        Update a horse's data.

        Args:
            horse_id (int): The ID of the horse.
            data (Dict): The data to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        horse = Horse.query.filter_by(id=horse_id)
        if not horse:
            return False
        horse.update(data)
        self.save()
        return True

    def delete(self, horse_id: int):
        """
        Delete a horse and its related data.

        Before deleting the horse we cascade delete every related data like HorseFiles and HorseTrainers.
        In workassignments we set the horse_id to null.

        Args:
            horse_id (int): The ID of the horse.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        horse = Horse.query.filter_by(id=horse_id)
        if not horse:
            return False
        horse.delete()
        self.save()
        return True

    def save(self):
        """
        Commit the current transaction.
        """
        self.db.session.commit()

    def get_trainers_of_horse(self, horse_id: int) -> List:
        """
        Get the trainers of a horse.

        Args:
            horse_id (int): The ID of the horse.

        Returns:
            List: The list of trainers.
        """
        horse_trainers = (self.db.session.query(HorseTrainers)
                          .filter(HorseTrainers.id_horse == horse_id).all())

        return (self.db.session.query(Employee)
                .filter(Employee.id.in_([ht.id_employee for ht in horse_trainers])).all())

    def add_horse_trainers(self, horse_id: int, trainers_ids: List[int]):
        """
        Add trainers to a horse.

        Args:
            horse_id (int): The ID of the horse.
            trainers_ids (List[int]): The list of trainer IDs.
        """
        for trainer_id in trainers_ids:
            self.db.session.add(HorseTrainers(id_horse=horse_id, id_employee=trainer_id))
        self.save()

    def add_document(self, horse_id: int, document: HorseFile):
        """
        Add a document to a horse.

        Args:
            horse_id (int): The ID of the horse.
            document (HorseFile): The document to add.
        """
        horse: Horse = self.__get_by_id(horse_id)
        horse.files.append(document)
        self.save()

    def __get_document_query(self, horse_id: int, document_id: int):
        """
        Get the query for a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            document_id (int): The ID of the document.

        Returns:
            Query: The query for the document.
        """
        query = (
            self.db.session.query(HorseFile)
            .filter_by(horse_id=horse_id, id=document_id)
        )
        return query

    def get_document(self, horse_id: int, document_id: int) -> Dict:
        """
        Get a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            document_id (int): The ID of the document.

        Returns:
            Dict: The document data.
        """
        doc = self.__get_document_query(horse_id, document_id).first()
        return doc.to_dict() if doc else {}

    def delete_document(self, horse_id: int, document_id) -> bool:
        """
        Delete a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            document_id (int): The ID of the document.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        horse: Horse = self.__get_by_id(horse_id)
        if not horse:
            return False
        doc_query = self.__get_document_query(horse.id, document_id)
        doc_query.delete()
        self.save()
        return True

    def get_file_page(
            self,
            horse_id: int,
            page: int,
            per_page: int,
            max_per_page: int = 10,
            search_query: Dict = None,
            order_by: List = None,
    ):
        """
        Get a paginated list of files for a horse.

        Args:
            horse_id (int): The ID of the horse.
            page (int): The page number.
            per_page (int): The number of items per page.
            max_per_page (int): The maximum number of items per page.
            search_query (Dict): The search query parameters.
            order_by (List): The order by parameters.

        Returns:
            Pagination: The paginated list of files.
        """
        query = HorseFile.query

        if search_query.get("filters"):
            search_query["filters"]["horse_id"] = horse_id
        else:
            search_query["filters"] = {"horse_id": horse_id}

        query = apply_filters(HorseFile, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def update_document(self, horse_id: int, document_id: int, data: Dict) -> bool:
        """
        Update a document of a horse.

        Args:
            horse_id (int): The ID of the horse.
            document_id (int): The ID of the document.
            data (Dict): The data to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        doc_query = self.db.session.query(HorseFile).filter_by(horse_id=horse_id, id=document_id)
        if not doc_query:
            return False
        doc_query.update(data)
        self.save()
        return True

    def remove_horse_trainer(self, horse_id: int, trainer_id: int) -> bool:
        """
        Remove a trainer from a horse.

        Args:
            horse_id (int): The ID of the horse.
            trainer_id (int): The ID of the trainer.

        Returns:
            bool: True if the removal was successful, False otherwise.
        """
        trainer = self.db.session.query(HorseTrainers).filter_by(id_horse=horse_id, id_employee=trainer_id)
        if not trainer:
            return False
        trainer.delete()
        self.save()
        return True

    def archive_horse(self, horse_id) -> bool:
        horse = Horse.query.get(horse_id)
        if not horse or horse.is_archived:
            return False
        horse.is_archived = True
        self.save()
        return True

    def recover_horse(self, horse_id) -> bool:
        horse = Horse.query.get(horse_id)
        if not horse or not horse.is_archived:
            return False
        horse.is_archived = False
        self.save()
        return True

    def get_horses(self):
        """
        Get all horses.

        Returns:
            List: The list of horses.
        """
        return Horse.query.all()

    def get_active_horses(self, page: int = 1, search: str = "", activity: str = "") -> bool:
        per_page = 7

        query = self.db.session.query(Horse).filter(Horse.is_deleted == False)

        if search:
            search_fields = ["name", "assigned_facility"]
            query = apply_multiple_search_criteria(
                Horse, query, search_query={"text": search, "fields": search_fields}
        )
        print(query.all())
        if activity:
            search_query = { "filters": { "ja_type": activity }}
            query = apply_filter_criteria(model=Horse, query=query, search_query=search_query)
        print(query.all())
        return query.paginate(page=page, per_page=per_page, error_out=False)
