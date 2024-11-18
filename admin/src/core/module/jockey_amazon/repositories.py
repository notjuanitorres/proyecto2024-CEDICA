"""
This module contains abstract and concrete repository classes for managing `JockeyAmazon` entities
and their associated documents and data.

Classes:
    AbstractJockeyAmazonRepository:
        Defines the abstract base class for repositories managing `JockeyAmazon` entities.
        This class contains method signatures for CRUD operations, document management,
        and other operations but does not provide their implementation.

    JockeyAmazonRepository:
        A concrete implementation of `AbstractJockeyAmazonRepository`, providing the actual
        logic to manage `JockeyAmazon` entities and documents.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from flask_sqlalchemy.pagination import Pagination

from src.core.database import db
from src.core.module.jockey_amazon.data import EducationLevelEnum
from src.core.module.jockey_amazon.models import JockeyAmazon, JockeyAmazonFile, FamilyMember
from src.core.module.common.repositories import apply_filters, apply_multiple_search_criteria
from src.core.module.employee.data import JobPositionEnum as Jobs


class AbstractJockeyAmazonRepository(ABC):
    """
    A concrete repository class for managing `JockeyAmazon` entities and their related operations.
    
    This class provides functionality to manage `JockeyAmazon` records, including adding, updating,
    retrieving, archiving, and deleting records. It also handles document management and specific
    assignment operations such as assigning employees and horses to jockeys.
    """

    def __init__(self):
        """
        Initializes the repository and sets up database access.
        """
        self.storage_path = "jockeys_amazons/"

    @abstractmethod
    def add(self, jockey: JockeyAmazon) -> JockeyAmazon:
        """
        Add a new `JockeyAmazon` entity to the database.

        Args:
            jockey (JockeyAmazon): The jockey entity to be added.

        Returns:
            JockeyAmazon: The added `JockeyAmazon` entity.
        """
        pass

    @abstractmethod
    def get_page(
        self,
        page: int,
        per_page: int,
        max_per_page: int,
        search_query: Dict = None,
        order_by: List = None,
    ):
        """
        Retrieve a paginated list of jockeys based on search criteria and sorting order.

        Args:
            page (int): The current page number.
            per_page (int): The number of records per page.
            max_per_page (int, optional): The maximum number of records per page. Defaults to 20.
            search_query (Dict, optional): Filters to apply to the query.
            order_by (List, optional): List of fields to order the results by.

        Returns:
            Pagination: A paginated result set of jockeys.
        """
        pass

    @abstractmethod
    def get_by_id(self, jockey_id: int) -> Optional[JockeyAmazon]:
        """
        Retrieve a `JockeyAmazon` entity by its ID.

        Args:
            jockey_id (int): The ID of the jockey.

        Returns:
            Optional[JockeyAmazon]: The `JockeyAmazon` entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def update(self, jockey_id: int, data: Dict) -> bool:
        """
        Update an existing `JockeyAmazon` entity by its ID with the given data.

        Args:
            jockey_id (int): The ID of the jockey to update.
            data (Dict): The data to update the entity with.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        pass

    @abstractmethod
    def archive(self, jockey_id: int) -> bool:
        """
        Archive a `JockeyAmazon` entity by setting its `is_deleted` flag to True.

        Args:
            jockey_id (int): The ID of the jockey to archive.

        Returns:
            bool: True if the jockey was successfully archived, False otherwise.
        """
        pass

    @abstractmethod
    def recover(self, jockey_id: int) -> bool:
        """
        Recover an archived `JockeyAmazon` entity by setting its `is_deleted` flag to False.

        Args:
            jockey_id (int): The ID of the jockey to recover.

        Returns:
            bool: True if the jockey was successfully recovered, False otherwise.
        """
        pass

    @abstractmethod
    def delete(self, jockey_id: int) -> bool:
        """
        Permanently delete a `JockeyAmazon` entity and its associated files.

        Args:
            jockey_id (int): The ID of the jockey to delete.

        Returns:
            bool: True if the jockey was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def add_document(self, jockey_id: int, document: JockeyAmazonFile):
        """
        Add a document to a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.
            document (JockeyAmazonFile): The document to add.
        """
        pass

    @abstractmethod
    def get_document(self, horse_id: int, document_id: int) -> Dict:
        """
        Retrieve a document for a specific jockey.

        Args:
            horse_id (int): The ID of the jockey.
            document_id (int): The ID of the document.

        Returns:
            Dict: Dictionary representation of the document, or None if not found.
        """
        pass

    @abstractmethod
    def delete_document(self, jockey_id: int, document_id: int):
        """
        Delete a document from a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.
            document_id (int): The ID of the document to delete.
        """
        pass

    @abstractmethod
    def get_file_page(
        self,
        jockey_id: int,
        page: int,
        per_page: int,
        max_per_page: int = 10,
        search_query: Dict = None,
        order_by: List = None,
    ):
        """
        Retrieve a paginated list of documents for a specific jockey.

        Args:
            jockey_id (int): The ID of the jockey.
            page (int): The current page number.
            per_page (int): The number of documents per page.
            max_per_page (int, optional): The maximum number of documents per page. Defaults to 10.
            search_query (Dict, optional): Filters to apply to the query.
            order_by (List, optional): List of fields to order the results by.

        Returns:
            Pagination: A paginated result set of documents.
        """
        pass

    @abstractmethod
    def update_document(self, jockey_id: int, document_id: int, data: Dict) -> bool:
        """
        Update a document for a specific jockey.

        Args:
            jockey_id (int): The ID of the jockey.
            document_id (int): The ID of the document to update.
            data (Dict): The data to update the document with.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        pass

    @abstractmethod
    def is_dni_used(self, dni: str) -> bool:
        """
        Check if a given DNI (national identification number) is already used by another jockey.

        Args:
            dni (str): The DNI of the jockey.

        Returns:
            bool: True if the DNI is already used, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def assign_employee(
        self, jockey_id: int, employee_id: int, employee_job_position: str
    ) -> bool:
        """
        Assign an employee to a jockey with a specific job position.

        Args:
            jockey_id (int): The ID of the jockey to assign the employee to.
            employee_id (int): The ID of the employee to be assigned.
            employee_job_position (str): The job position of the employee being assigned.

        Returns:
            bool: True if the employee was successfully assigned, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def unassign_employee(self, jockey_id: int, link_to: str) -> bool:
        """
        Unassign an employee from a jockey by a specific link or relationship.

        Args:
            jockey_id (int): The ID of the jockey from whom the employee is being unassigned.
            link_to (str): The relationship or job position to unassign.

        Returns:
            bool: True if the employee was successfully unassigned, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def assign_horse(self, jockey_id: int, horse_id: int) -> bool:
        """
        Assign a horse to a jockey.

        Args:
            jockey_id (int): The ID of the jockey to whom the horse is assigned.
            horse_id (int): The ID of the horse to be assigned to the jockey.

        Returns:
            bool: True if the horse was successfully assigned, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def unassign_horse(self, jockey_id: int) -> bool:
        """
        Unassign the current horse from a jockey.

        Args:
            jockey_id (int): The ID of the jockey from whom the horse is being unassigned.

        Returns:
            bool: True if the horse was successfully unassigned, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def toggle_debtor_status(self, jockey_id: int) -> bool:
        """
        Toggle the debtor status of a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.

        Returns:
            bool: True if the status was successfully toggled, False otherwise.
        """
        pass

    @abstractmethod
    def count_id_in_charges(self, jockey_id: int) -> int:
        """Count the number of charges that have the jockey_id

        Args:
            jockey_id (int): The jockey id

        Returns:
            int: The number of charges that have the jockey_id
        """
        pass

    @abstractmethod
    def get_active_jockeys(
            self, page: int = 1, search: str = ""
    ) -> Pagination:
        """
        Retrieve a paginated list of not deleted jockeys filtered by an optional search term.

        Args:
            page (int, optional): The page number for pagination. Defaults to 1.
            search (str, optional): A search term to filter employees by name or email.
                                    Defaults to an empty string.

        Returns:
            Pagination: A Flask-SQLAlchemy Pagination object containing the active employees
                         that match the provided filters.

        Raises:
            NotImplementedError: If the method is not implemented in a derived class.
        """
        raise NotImplementedError


class JockeyAmazonRepository(AbstractJockeyAmazonRepository):
    """
    Concrete implementation of AbstractJockeyAmazonRepository for managing `JockeyAmazon` entities.
    """

    def __init__(self):
        """
        Initializes the repository and sets the database connection.
        """
        super().__init__()
        self.db = db

    def __get_by_dni(self, dni: str) -> JockeyAmazon | None:
        """
        Retrieve a `JockeyAmazon` entity by its DNI.

        Args:
            dni (str): The DNI of the jockey.

        Returns:
            JockeyAmazon | None: The `JockeyAmazon` entity if found, otherwise None.
        """
        return (
            self.db.session.query(JockeyAmazon).filter(JockeyAmazon.dni == dni).first()
        )

    def add(self, jockey: JockeyAmazon) -> JockeyAmazon:
        """
        Add a new `JockeyAmazon` entity to the database.

        Args:
            jockey (JockeyAmazon): The jockey entity to be added.

        Returns:
            JockeyAmazon: The added `JockeyAmazon` entity.
        """
        self.db.session.add(jockey)
        self.db.session.flush()
        self.save()
        return jockey

    def get_page(
        self,
        page: int,
        per_page: int,
        max_per_page: int = 20,
        search_query: Dict = None,
        order_by: List = None,
    ):
        """
        Retrieve a paginated list of `JockeyAmazon` entities based on search criteria and sorting order.

        Args:
            page (int): The current page number.
            per_page (int): The number of records per page.
            max_per_page (int, optional): The maximum number of records per page. Defaults to 20.
            search_query (Dict, optional): Filters to apply to the query.
            order_by (List, optional): List of fields to order the results by.

        Returns:
            Pagination: A paginated result set of `JockeyAmazon` entities.
        """
        query = JockeyAmazon.query

        query = apply_filters(JockeyAmazon, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, jockey_id: int) -> Optional[JockeyAmazon]:
        """
        Retrieve a `JockeyAmazon` entity by its ID.

        Args:
            jockey_id (int): The ID of the jockey.

        Returns:
            Optional[JockeyAmazon]: The `JockeyAmazon` entity if found, otherwise None.
        """
        return (
            self.db.session.query(JockeyAmazon)
            .filter(JockeyAmazon.id == jockey_id)
            .first()
        )

    def update(self, jockey_id: int, data: Dict) -> bool:
        """
        Update a `JockeyAmazon` entity with the provided data.

        Args:
            jockey_id (int): The ID of the jockey.
            data (Dict): The data to update the jockey with.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        jockey = JockeyAmazon.query.filter_by(id=jockey_id)
        if not jockey:
            return False
        jockey.update(data)
        self.save()
        return True

    def archive(self, jockey_id: int) -> bool:
        """
        Archive a `JockeyAmazon` entity by setting its `is_deleted` flag to True.

        Args:
            jockey_id (int): The ID of the jockey to archive.

        Returns:
            bool: True if the jockey was successfully archived, False otherwise.
        """
        jockey = self.get_by_id(jockey_id)
        if not jockey or jockey.is_deleted:
            return False
        jockey.is_deleted = True
        self.save()
        return True

    def recover(self, jockey_id: int) -> bool:
        """
        Recover an archived `JockeyAmazon` entity by setting its `is_deleted` flag to False.

        Args:
            jockey_id (int): The ID of the jockey to recover.

        Returns:
            bool: True if the jockey was successfully recovered, False otherwise.
        """
        jockey = self.get_by_id(jockey_id)
        if not jockey or not jockey.is_deleted:
            return False
        jockey.is_deleted = False
        self.save()
        return True

    def delete(self, jockey_id: int) -> bool:
        """
        Permanently delete a `JockeyAmazon` entity and its associated files.

        Args:
            jockey_id (int): The ID of the jockey to delete.

        Returns:
            bool: True if the jockey was successfully deleted, False otherwise.
        """
        jockey = JockeyAmazon.query.filter_by(id=jockey_id)
        if not jockey:
            return False

        files = JockeyAmazonFile.query.filter_by(jockey_amazon_id=jockey_id)
        minio_path_files = [f.path for f in files if not f.is_link]
        if minio_path_files:
            from src.core.container import Container  # can't import outside due to circular import
            success = Container().storage_services().delete_batch(minio_path_files)

            if not success:
                return False
        jockey.delete()
        self.save()
        return True

    def save(self):
        """
        Commit the current session to the database.
        """
        self.db.session.commit()

    def add_document(self, jockey_id: int, document: JockeyAmazonFile):
        """
        Add a document to a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.
            document (JockeyAmazonFile): The document to add.
        """
        jockey: JockeyAmazon = self.get_by_id(jockey_id)
        jockey.files.append(document)
        self.save()

    def get_all(self):
        """
        Retrieve all `JockeyAmazonFile` entities.

        Returns:
            List[JockeyAmazonFile]: A list of all `JockeyAmazonFile` entities.
        """
        return self.db.session.query(JockeyAmazonFile).all()

    def __get_query_document(self, jockey_id: int, document_id: int):
        """
        Retrieve a query for a specific document of a jockey.

        Args:
            jockey_id (int): The ID of the jockey.
            document_id (int): The ID of the document.

        Returns:
            Query: The query object for the document.
        """
        query = self.db.session.query(JockeyAmazonFile).filter_by(
            jockey_amazon_id=jockey_id, id=document_id
        )
        return query

    def get_document(self, horse_id: int, document_id: int) -> Dict:
        """
        Retrieve a document for a specific jockey.

        Args:
            horse_id (int): The ID of the jockey.
            document_id (int): The ID of the document.

        Returns:
            Dict: The document data if found, otherwise None.
        """
        doc = self.__get_query_document(horse_id, document_id).first()
        return doc.to_dict() if doc else doc

    def delete_document(self, jockey_id: int, document_id: int):
        """
        Delete a document from a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.
            document_id (int): The ID of the document to delete.
        """
        jockey: JockeyAmazon = self.get_by_id(jockey_id)
        document = self.__get_query_document(jockey.id, document_id)
        document.delete()
        self.save()

    def get_file_page(
        self,
        jockey_id: int,
        page: int,
        per_page: int,
        max_per_page: int = 10,
        search_query: Dict = None,
        order_by: List = None,
    ):
        """
        Retrieve a paginated list of documents for a specific jockey.

        Args:
            jockey_id (int): The ID of the jockey.
            page (int): The current page number.
            per_page (int): The number of documents per page.
            max_per_page (int, optional): The maximum number of documents per page. Defaults to 10.
            search_query (Dict, optional): Filters to apply to the query.
            order_by (List, optional): List of fields to order the results by.

        Returns:
            Pagination: A paginated result set of documents.
        """
        query = JockeyAmazonFile.query

        if search_query.get("filters"):
            search_query["filters"]["jockey_amazon_id"] = jockey_id
        else:
            search_query["filters"] = {"jockey_amazon_id": jockey_id}

        query = apply_filters(JockeyAmazonFile, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def update_document(self, jockey_id: int, document_id: int, data: Dict) -> bool:
        """
        Update a document for a specific jockey.

        Args:
            jockey_id (int): The ID of the jockey.
            document_id (int): The ID of the document to update.
            data (Dict): The data to update the document with.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        doc_query = self.db.session.query(JockeyAmazonFile).filter_by(
            jockey_amazon_id=jockey_id, id=document_id
        )
        if not doc_query:
            return False
        doc_query.update(data)
        self.save()
        return True

    def toggle_debtor_status(self, jockey_id: int) -> bool:
        """
        Toggle the debtor status of a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.

        Returns:
            bool: True if the status was successfully toggled, False otherwise.
        """
        jockey: JockeyAmazon = self.get_by_id(jockey_id)
        if not jockey:
            return False
        jockey.has_debts = not jockey.has_debts
        self.save()
        return True

    def update_school_information(self, jockey_id: int, data: Dict) -> bool:
        """
        Update the school information for a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.
            data (Dict): The updated school information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        jockey = JockeyAmazon.query.get(jockey_id)
        if not jockey:
            return False

        school_data = data.get("school_institution", {})
        for key, value in school_data.items():
            if hasattr(jockey.school_institution, key):
                setattr(jockey.school_institution, key, value)

        jockey.current_grade_year = data.get(
            "current_grade_year", jockey.current_grade_year
        )
        jockey.school_observations = data.get(
            "school_observations", jockey.school_observations
        )

        self.save()

        return True

    def update_family_information(self, jockey_id: int, data: Dict) -> bool:
        jockey = self.get_by_id(jockey_id)
        if not jockey:
            return False
        jockey.has_family_assignment = data.get('has_family_assignment', jockey.has_family_assignment)
        jockey.family_assignment_type = data.get('family_assignment_type', jockey.family_assignment_type)
        jockey.has_pension = data.get('has_pension', jockey.has_pension)
        jockey.pension_type = data.get('pension_type', jockey.pension_type)
        jockey.pension_details = data.get('pension_details', jockey.pension_details)
        updated_members = [member_data for member_data in data.get("family_members") if member_data.get('id')]
        for member_data in updated_members:
            print(member_data.get("education_level"))
            existing_member = FamilyMember.query.get(member_data.get("id"))
            if existing_member:
                print(existing_member.education_level.name)
                existing_member.relationship = member_data.get('relationship', existing_member.relationship)
                existing_member.first_name = member_data.get('first_name', existing_member.first_name)
                existing_member.last_name = member_data.get('last_name', existing_member.last_name)
                existing_member.street = member_data.get('street', existing_member.street)
                existing_member.number = member_data.get('number', existing_member.number)
                existing_member.department = member_data.get('department', existing_member.department)
                existing_member.locality = member_data.get('locality', existing_member.locality)
                existing_member.province = member_data.get('province', existing_member.province)
                existing_member.phone_country_code = member_data.get('phone_country_code', existing_member.phone_country_code)
                existing_member.phone_area_code = member_data.get('phone_area_code', existing_member.phone_area_code)
                existing_member.phone_number = member_data.get('phone_number', existing_member.phone_number)
                existing_member.email = member_data.get('email', existing_member.email)
                existing_member.education_level = EducationLevelEnum[member_data.get('education_level', existing_member.education_level.name)]
                existing_member.occupation = member_data.get('occupation', existing_member.occupation)
                self.db.session.add(existing_member)
                self.save()
                return True

    def update_assignments(self, jockey_id: int, data: Dict) -> bool:
        """
        Update the work assignments for a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.
            data (Dict): The updated assignment data.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        jockey = JockeyAmazon.query.get(jockey_id)
        if not jockey:
            return False
        assignment = jockey.work_assignment

        if assignment and data:
            assignment_data = data.get("work_assignments", {})
            for key, value in assignment_data.items():
                setattr(assignment, key, value)

        jockey.has_scholarship = data.get("has_scholarship")
        jockey.scholarship_observations = data.get("scholarship_observations")
        jockey.scholarship_percentage = data.get("scholarship_percentage")
        self.db.session.add(assignment)
        self.db.session.add(jockey)
        assignment.days = assignment_data.get("days", [])
        self.save()
        return True

    def is_dni_used(self, dni: str) -> bool:
        """
        Check if a DNI is already used by a `JockeyAmazon` entity.

        Args:
            dni (str): The DNI to check.

        Returns:
            bool: True if the DNI is used, False otherwise.
        """
        return self.__get_by_dni(dni) is not None

    def assign_employee(
        self, jockey_id: int, employee_id: int, employee_job_position: str
    ):
        """
        Assign an employee to a `JockeyAmazon` entity based on the job position.

        Args:
            jockey_id (int): The ID of the jockey.
            employee_id (int): The ID of the employee.
            employee_job_position (str): The job position of the employee.

        Returns:
            bool: True if the employee was successfully assigned, False otherwise.
        """
        jockey = self.get_by_id(jockey_id)
        if not jockey:
            return False
        if employee_job_position in {Jobs.PROFESOR_EQUITACION.name, Jobs.TERAPEUTA.name}:
            jockey.work_assignment.professor_or_therapist_id = employee_id
        elif employee_job_position == Jobs.AUXILIAR_PISTA.name:
            jockey.work_assignment.track_assistant_id = employee_id
        elif employee_job_position == Jobs.CONDUCTOR.name:
            jockey.work_assignment.conductor_id = employee_id
        else:
            return False
        self.save()
        return True

    def assign_horse(self, jockey_id: int, horse_id: int):
        """
        Assign a horse to a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.
            horse_id (int): The ID of the horse.

        Returns:
            bool: True if the horse was successfully assigned, False otherwise.
        """
        jockey = self.get_by_id(jockey_id)
        if not jockey:
            return False
        jockey.work_assignment.horse_id = horse_id
        self.save()
        return True

    def unassign_employee(self, jockey_id: int, link_to: str):
        """
        Unassign an employee from a `JockeyAmazon` entity based on the job position or horse assignment.

        Args:
            jockey_id (int): The ID of the jockey.
            link_to (str): The type of assignment (e.g., job position or horse).

        Returns:
            bool: True if the employee was successfully unassigned, False otherwise.
        """
        jockey = self.get_by_id(jockey_id)
        if not jockey:
            return False
        if link_to in {Jobs.PROFESOR_EQUITACION.name, Jobs.TERAPEUTA.name}:
            jockey.work_assignment.professor_or_therapist_id = None
        elif link_to == Jobs.AUXILIAR_PISTA.name:
            jockey.work_assignment.track_assistant_id = None
        elif link_to == Jobs.CONDUCTOR.name:
            jockey.work_assignment.conductor_id = None
        elif link_to == "Horse":
            jockey.work_assignment.horse_id = None
        else:
            return False

        self.save()
        return True
    
    def unassign_horse(self, jockey_id: int) -> bool:
        """
        Unassign a horse from a `JockeyAmazon` entity.

        Args:
            jockey_id (int): The ID of the jockey.

        Returns:
            bool: True if the horse was successfully unassigned, False otherwise.
        """
        jockey = self.get_by_id(jockey_id)
        if not jockey:
            return False
        jockey.work_assignment.horse_id = None
        self.save()
        return True

    def count_id_in_charges(self, jockey_id: int) -> int:
        from src.core.module.charges.models import Charge  # can't import outside due to circular import

        return Charge.query.filter_by(jya_id=jockey_id).count()

    def get_active_jockeys(
            self, page: int = 1, search: str = ""
    ) -> Pagination:
        """Retrieve a paginated list of not deleted jockeys filtered by search text."""

        per_page = 7
        query = self.db.session.query(JockeyAmazon).filter_by(is_deleted=False)
        if search:
            search_fields = ["first_name", "last_name", "dni"]
            query = apply_multiple_search_criteria(
                JockeyAmazon, query, search_query={"text": search, "fields": search_fields}
            )
        return query.paginate(page=page, per_page=per_page, error_out=False)
