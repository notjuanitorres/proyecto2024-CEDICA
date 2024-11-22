"""
This module defines the abstract base class and the concrete class for 
employee repository operations.

Serves as a repository class that handle employee-related database operations, 
including  CRUD (Create, Read, Update, Delete) functionalities, document management, 
and specialized queries for various employee types such as trainers.
"""

from typing import Dict, List
from abc import abstractmethod
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.pagination import Pagination
from dependency_injector.wiring import Provide, inject
from src.core.database import db as database
from src.core.module.common.repositories import (
    apply_filters,
    apply_multiple_search_criteria,
    apply_filter_criteria
)
from src.core.module.common import AbstractStorageServices
from src.core.module.charges.models import Charge
from src.core.module.payment.models import Payment
from src.core.module.equestrian.models import HorseTrainers
from src.core.module.user.models import User


from src.core.module.employee.mappers import EmployeeMapper as Mapper
from src.core.module.employee.models import Employee, EmployeeFile
from src.core.module.employee.data import JobPositionEnum as PositionEnum


class AbstractEmployeeRepository:
    """
    Abstract base class defining the interface for employee operations.

    This class provides the contract for implementing employee-related database operations
    including CRUD operations, document management, and specialized queries for trainers
    and other employee types.

    Attributes:
        storage_path (str): Base path for storing employee files in S3 Storage.
    """

    def __init__(self):
        """Initialize the repository with default storage path."""
        self.storage_path = "employees/"

    @abstractmethod
    def add(self, employee: Employee) -> Employee | None:
        """
        Add a new employee to the repository.

        Args:
            employee: Employee instance to be added.

        Returns:
            Employee: Added employee data if successful, None otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def get_page(
        self,
        page: int,
        per_page: int,
        max_per_page: int,
        search_query: Dict = None,
        order_by: list = None,
    ) -> Pagination:
        """Retrieve a paginated list of employees.

        Args:
            page: Page number to retrieve.
            per_page: Number of items per page.
            max_per_page: Maximum allowed items per page.
            search_query: Optional search criteria.
            order_by: Optional sorting criteria.

        Returns:
            Pagination: Paginated employee results.
        """
        raise NotImplementedError

    @abstractmethod
    def get_active_employees(
        self, job_positions: list[str], page: int = 1, search: str = ""
    ) -> Pagination:
        """
        Retrieve a paginated list of active and not deleted employees filtered by job positions
        and an optional search term.

        Args:
            job_positions (List[str]): A list of job positions to filter the employees.
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

    @abstractmethod
    def get_employee(self, employee_id: int, documents: bool = True) -> Dict:
        """
        Retrieve a single employee by ID with optional documents inclusion.

        Args:
            employee_id: ID of the employee to retrieve.
            documents: Include associated documents if True.

        Returns:
            Pagination: SQLAlchemy pagination object with 7 items per page.
        """
        raise NotImplementedError

    @abstractmethod
    def is_email_used(self, email: str) -> bool:
        """Check if an email address is already registered.

        Args:
            email: Email address to check.

        Returns:
            bool: True if email is in use, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def is_dni_used(self, dni: str) -> bool:
        """Check if a DNI (national ID) is already registered.

        Args:
            dni: DNI number to check.

        Returns:
            bool: True if DNI is in use, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, employee_id: int, data: Dict) -> bool:
        """Update an employee's information.

        Args:
            employee_id: ID of the employee to update.
            data: Dictionary containing updated employee data.

        Returns:
            bool: True if update successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def archive(self, employee_id):
        """Mark an employee as archived.

        Args:
            employee_id: ID of the employee to archive.

        Returns:
            bool: True if archival successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def recover(self, employee_id):
        """Recover an archived employee.

        Args:
            employee_id: ID of the employee to recover.

        Returns:
            bool: True if recovery successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, employee_id: int) -> bool:
        """Permanently delete an employee.

        Args:
            employee_id: ID of the employee to delete.

        Returns:
            bool: True if deletion successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def add_document(self, employee_id: int, document: EmployeeFile) -> None:
        """Add a document to an employee's file.

        Args:
            employee_id: ID of the employee.
            document: EmployeeFile instance to add.
        """
        raise NotImplementedError

    @abstractmethod
    def get_document(self, employee_id: int, document_id: int) -> EmployeeFile:
        """
        Retrieve a specific employee document.

        Args:
            employee_id: ID of the employee.
            document_id: ID of the document to retrieve.

        Returns:
            EmployeeFile: Retrieved document.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_document(self, employee_id: int, document_id: int) -> None:
        """
        Delete a specific employee document.

        Args:
            employee_id: ID of the employee.
            document_id: ID of the document to delete.
        """
        raise NotImplementedError

    @abstractmethod
    def update_document(self, employee_id: int, document_id: int, data: Dict) -> bool:
        """
        Update a specific employee document.

        Args:
            employee_id: ID of the employee.
            document_id: ID of the document to update.
            data: Updated document data.

        Returns:
            bool: True if update successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def get_file_page(
        self,
        employee_id: int,
        page: int,
        per_page: int,
        max_per_page: int = 10,
        search_query: Dict = None,
        order_by: List = None,
    ):
        """
        Retrieve a paginated list of employee documents.

        Args:
            employee_id: ID of the employee.
            page: Page number to retrieve.
            per_page: Number of items per page.
            max_per_page: Maximum allowed items per page.
            search_query: Optional search criteria.
            order_by: Optional sorting criteria.

        Returns:
            Pagination: Paginated document results.
        """
        raise NotImplementedError

    @abstractmethod
    def get_paginated_trainers(
        self,
        page: int,
        per_page: int = 7,
        max_per_page: int = 10,
        search_query: Dict = None,
        order_by: List = None,
    ) -> Pagination:
        """
        Retrieve a paginated list of horse trainers.

        Args:
            page: Page number to retrieve.
            per_page: Number of items per page.
            max_per_page: Maximum allowed items per page.
            search_query: Optional search criteria.
            order_by: Optional sorting criteria.

        Returns:
            Pagination: Paginated trainer results.
        """
        raise NotImplementedError

    @abstractmethod
    def link_account(self, employee_id: int, account_id: int | None) -> bool:
        """
        Link or unlink an employee to a user account.

        Args:
            employee_id: ID of the employee.
            account_id: ID of the account to link, or None to unlink.

        Returns:
            bool: True if operation successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def toggled_activation(self, employee_id: int) -> bool:
        """
        Toggle the active status of an employee.

        Args:
            employee_id: ID of the employee.

        Returns:
            bool: New active status.
        """
        raise NotImplementedError

    @abstractmethod
    def is_employee_active(self, employee_id: int) -> bool:
        """
        Check if an employee is currently active.

        Args:
            employee_id: ID of the employee.

        Returns:
            bool: True if employee is active, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def count_id_in_charges_and_payments(self, employee_id: int) -> int:
        """
        Count the number of times an employee ID is present in charges or payments.

        Args:
            employee_id: ID of the employee.

        Returns:
            int: Number of times the employee ID is present in other entities.
        """
        raise NotImplementedError


class EmployeeRepository(AbstractEmployeeRepository):
    """
    Concrete implementation of the employee repository.

    This class implements all abstract methods defined in AbstractEmployeeRepository,
    providing actual database operations using SQLAlchemy.
    """

    def __init__(self, storage_services: AbstractStorageServices):
        """Initialize the repository with database connection."""
        super().__init__()
        self.db: SQLAlchemy = database
        self.storage_services = storage_services

    def __get_by_id(self, employee_id: int) -> Employee:
        """Internal method to retrieve an employee by ID."""

        return (
            self.db.session.query(Employee).filter(Employee.id == employee_id).first()
        )

    def __get_by_email(self, email: str) -> Employee | None:
        """Internal method to retrieve an employee by email."""

        return self.db.session.query(Employee).filter(Employee.email == email).first()

    def __get_by_dni(self, dni: str) -> Employee | None:
        """Internal method to retrieve an employee by DNI."""

        return self.db.session.query(Employee).filter(Employee.dni == dni).first()

    def __get_query_trainers(self, query):
        """Internal method to filter query for trainers."""

        return query.filter(
            or_(
                Employee.position == PositionEnum["CONDUCTOR"],
                Employee.position == PositionEnum["ENTRENADOR_CABALLOS"],
            )
        )

    def __get_document_query(self, employee_id: int, document_id: int):
        """Internal method to filter query for files."""

        query = self.db.session.query(EmployeeFile).filter_by(
            employee_id=employee_id, id=document_id
        )
        return query

    def save(self):
        """Commit current transaction to the database."""
        self.db.session.commit()

    def add(self, employee: Employee):
        """Add a new employee to the database and return mapped entity."""

        self.db.session.add(employee)
        self.db.session.flush()
        self.save()

        return Mapper.from_entity(employee)

    def get_page(
        self,
        page: int = 1,
        per_page: int = 10,
        max_per_page: int = 30,
        search_query: Dict = None,
        order_by: List = None,
    ):
        """Retrieve a paginated list of employees with filtered search and ordering."""

        per_page = 10
        max_per_page = 30
        query = Employee.query

        query = apply_filters(Employee, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_employee(self, employee_id, documents=True):
        """Retrieve a single employee by ID with optional documents inclusion."""

        return Mapper.from_entity(self.__get_by_id(employee_id), documents=documents)

    def update(self, employee_id: int, data: Dict) -> bool:
        """Update an employee's information."""

        employee = Employee.query.filter_by(id=employee_id)
        if not employee:
            return False
        employee.update(data)
        self.save()
        return True

    def archive(self, employee_id):
        """Mark an employee as archived and deactivate their account."""

        employee = Employee.query.get(employee_id)
        if not employee or employee.is_deleted:
            return False
        employee.is_deleted = True
        employee.is_active = False
        if employee.user_id:
            User.query.get(employee.user_id).enabled = False
        self.save()
        return True

    def recover(self, employee_id):
        """Recover an archived employee."""

        employee = Employee.query.get(employee_id)
        if not employee or not employee.is_deleted:
            return False
        employee.is_deleted = False
        if employee.user_id:
            User.query.get(employee.user_id).enabled = True
        self.save()
        return True

    def delete(self, employee_id):
        """Permanently delete an employee record and its associated files."""

        employee = Employee.query.get(employee_id)
        if not employee:
            return False

        files = EmployeeFile.query.filter_by(employee_id=employee_id)
        minio_path_files = [f.path for f in files if not f.is_link]
        if minio_path_files:
            success = self.storage_services.delete_batch(minio_path_files)

            if not success:
                return False

        self.db.session.delete(employee)
        self.save()
        return True

    def is_email_used(self, email: str) -> bool:
        """Check if email address is already registered to an employee."""

        return self.__get_by_email(email) is not None

    def is_dni_used(self, dni: str) -> bool:
        """Check if DNI (national ID) is already registered to an employee."""

        return self.__get_by_dni(dni) is not None

    def add_document(self, employee_id: int, document: EmployeeFile):
        """Retrieve a specific employee document."""

        employee: Employee = self.__get_by_id(employee_id)
        employee.files.append(document)
        self.save()

    def get_document(self, employee_id: int, document_id: int) -> Dict:
        """Retrieve a specific employee document."""

        doc = self.__get_document_query(employee_id, document_id).first()
        return doc.to_dict() if doc else {}

    def delete_document(self, employee_id: int, document_id):
        """Delete a specific document from an employee's file collection."""

        employee: Employee = self.__get_by_id(employee_id)
        doc_query = self.__get_document_query(employee.id, document_id)
        doc_query.delete()
        self.save()

    def get_file_page(
        self,
        employee_id: int,
        page: int,
        per_page: int,
        max_per_page: int = 10,
        search_query: Dict = None,
        order_by: List = None,
    ):
        """Retrieve a paginated list of documents for a specific employee."""

        query = EmployeeFile.query
        if search_query.get("filters"):
            search_query["filters"]["employee_id"] = employee_id
        else:
            search_query["filters"] = {"employee_id": employee_id}
        query = apply_filters(EmployeeFile, query, search_query, order_by)
        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def update_document(self, employee_id: int, document_id: int, data: Dict) -> bool:
        """Update a specific employee document."""

        doc_query = self.db.session.query(EmployeeFile).filter_by(
            employee_id=employee_id, id=document_id
        )
        if not doc_query:
            return False
        doc_query.update(data)
        self.save()
        return True

    def link_account(self, employee_id: int, account_id: int | None) -> bool:
        """Toggle the active status of an employee."""

        employee = self.__get_by_id(employee_id=employee_id)
        if not employee:
            return False
        employee.user_id = account_id
        self.save()
        return True

    def toggled_activation(self, employee_id: int) -> bool:
        """Toggle the active status of an employee."""

        employee = self.__get_by_id(employee_id)
        employee.is_active = not employee.is_active
        self.save()
        return employee.is_active

    def is_employee_active(self, employee_id: int) -> bool:
        """Check if an employee is currently active."""

        if not employee_id:
            return False
        employee = self.__get_by_id(employee_id)
        return employee.is_active

    def get_active_employees(
        self, job_positions: list[str], page: int = 1, search: str = ""
    ):
        """Retrieve a paginated list of active and not deleted employees filtered by position and search text."""

        per_page = 7
        query = self.db.session.query(Employee)
        query = apply_filter_criteria(Employee, query, {"filters": {"is_active": True, "is_deleted": False}})
        if job_positions:
            query = query.filter(Employee.position.in_(job_positions))
        if search:
            search_fields = ["name", "lastname", "email", "dni"]
            query = apply_multiple_search_criteria(
                Employee, query, search_query={"text": search, "fields": search_fields}
            )
        return query.paginate(page=page, per_page=per_page, error_out=False)

    def get_paginated_trainers(
        self,
        page: int,
        per_page: int = 7,
        max_per_page: int = 10,
        search_query: Dict = None,
        order_by: List = None,
    ) -> Pagination:

        query = Employee.query

        if search_query.get("filters"):
            if search_query.get("filters").get("only_horse_id"):
                # Get trainers that are already assigned to the horse
                query2 = HorseTrainers.query.filter_by(
                    id_horse=search_query["filters"]["only_horse_id"]
                )
                ids_employees = [ht.id_employee for ht in query2.all()]

                # Get them using previous query
                query = query.filter(Employee.id.in_(ids_employees))

                return query.paginate(
                    page=page,
                    per_page=per_page,
                    error_out=False,
                    max_per_page=max_per_page,
                )

            if search_query.get("filters").get("not_horse_id"):
                # Get trainers that are already assigned to the horse
                query2 = HorseTrainers.query.filter_by(
                    id_horse=search_query["filters"]["not_horse_id"]
                )
                ids_employees = [ht.id_employee for ht in query2.all()]

                # Remove them
                query = query.filter(Employee.id.notin_(ids_employees))

        query = self.__get_query_trainers(query)
        query = apply_filters(
            Employee,
            query,
            search_query,
            order_by,
        )

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def count_id_in_charges_and_payments(self, employee_id: int) -> int:
        """Count the number of times an employee ID is present in charges or payments."""

        return (
            Charge.query.filter_by(employee_id=employee_id).count()
            + Payment.query.filter_by(beneficiary_id=employee_id).count()
        )
