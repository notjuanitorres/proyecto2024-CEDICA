from typing import Dict, List
from abc import abstractmethod
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.pagination import Pagination
from src.core.database import db as database
from src.core.module.employee.models import Employee, EmployeeFile
from src.core.module.common.repositories import apply_filters
from src.core.module.employee.data import JobPositionEnum as PositionEnum
from .mappers import EmployeeMapper as Mapper
from ..equestrian.models import HorseTrainers


class AbstractEmployeeRepository:
    def __init__(self):
        self.storage_path = "employees/"

    @abstractmethod
    def add(self, employee: Employee) -> Employee | None:
        pass

    @abstractmethod
    def get_page(
        self,
        page: int,
        per_page: int,
        max_per_page: int,
        search_query: Dict = None,
        order_by: list = None,
    ) -> Pagination:
        raise NotImplementedError

    @abstractmethod
    def get_employee(self, employee_id: int, documents: bool = True) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def is_email_used(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_dni_used(self, dni: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, employee_id: int, data: Dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def archive(self, employee_id):
        raise NotImplementedError

    @abstractmethod
    def recover(self, employee_id):
        raise NotImplementedError

    @abstractmethod
    def delete(self, employee_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_document(self, employee_id: int, document: EmployeeFile) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_document(self, employee_id: int, document_id: int) -> EmployeeFile:
        raise NotImplementedError

    @abstractmethod
    def delete_document(self, employee_id: int, document_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_document(self, employee_id: int, document_id: int, data: Dict) -> bool:
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
        raise NotImplementedError

    @abstractmethod
    def link_account(self, employee_id: int, account_id: int | None) -> bool:
        pass

    @abstractmethod
    def toggled_activation(self, employee_id: int) -> bool:
        pass

    @abstractmethod
    def is_employee_active(self, employee_id: int) -> bool:
        pass


class EmployeeRepository(AbstractEmployeeRepository):
    def __init__(self):
        super().__init__()
        self.db: SQLAlchemy = database

    def save(self):
        self.db.session.commit()

    def add(self, employee: Employee):
        self.db.session.add(employee)
        self.db.session.flush()
        self.save()

        return Mapper.from_entity(employee)

    def __get_by_id(self, employee_id: int) -> Employee:
        return (
            self.db.session.query(Employee).filter(Employee.id == employee_id).first()
        )

    def __get_by_email(self, email: str) -> Employee | None:
        return self.db.session.query(Employee).filter(Employee.email == email).first()

    def __get_by_dni(self, dni: str) -> Employee | None:
        return self.db.session.query(Employee).filter(Employee.dni == dni).first()

    def get_page(
        self,
        page: int = 1,
        per_page: int = 10,
        max_per_page: int = 30,
        search_query: Dict = None,
        order_by: List = None,
    ):
        per_page = 10
        max_per_page = 30
        query = Employee.query

        query = apply_filters(Employee, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_employee(self, employee_id, documents=True):
        return Mapper.from_entity(self.__get_by_id(employee_id), documents=documents)

    def update(self, employee_id: int, data: Dict) -> bool:
        employee = Employee.query.filter_by(id=employee_id)
        if not employee:
            return False
        employee.update(data)
        self.save()
        return True

    def archive(self, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee or employee.is_deleted:
            return False
        employee.is_deleted = True
        employee.is_active = False
        employee.user_id = None
        self.save()
        return True

    def recover(self, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee or not employee.is_deleted:
            return False
        employee.is_deleted = False
        self.save()
        return True

    def delete(self, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            return False
        self.db.session.delete(employee)
        self.save()
        return True

    def is_email_used(self, email: str) -> bool:
        return self.__get_by_email(email) is not None

    def is_dni_used(self, dni: str) -> bool:
        return self.__get_by_dni(dni) is not None

    def add_document(self, employee_id: int, document: EmployeeFile):
        employee: Employee = self.__get_by_id(employee_id)
        employee.files.append(document)
        self.save()

    def __get_document_query(self, employee_id: int, document_id: int):
        query = self.db.session.query(EmployeeFile).filter_by(
            employee_id=employee_id, id=document_id
        )
        return query

    def get_document(self, employee_id: int, document_id: int) -> Dict:
        doc = self.__get_document_query(employee_id, document_id).first()
        return doc.to_dict() if doc else {}

    def delete_document(self, employee_id: int, document_id):
        employee: Employee = self.__get_by_id(employee_id)
        doc_query = self.__get_document_query(employee.id, document_id)
        doc_query.delete()
        self.save()

    def __get_query_trainers(self, query):
        return query.filter(
            or_(
                Employee.position == PositionEnum["CONDUCTOR"],
                Employee.position == PositionEnum["ENTRENADOR_CABALLOS"],
            )
        )

    def get_file_page(
        self,
        employee_id: int,
        page: int,
        per_page: int,
        max_per_page: int = 10,
        search_query: Dict = None,
        order_by: List = None,
    ):

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
        doc_query = self.db.session.query(EmployeeFile).filter_by(
            employee_id=employee_id, id=document_id
        )
        if not doc_query:
            return False
        doc_query.update(data)
        self.save()
        return True

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

                # Get them
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

    def link_account(self, employee_id: int, account_id: int | None) -> bool:
        employee = self.__get_by_id(employee_id=employee_id)
        if not employee:
            return False
        employee.user_id = account_id
        self.save()
        return True

    def toggled_activation(self, employee_id: int) -> bool:
        employee = self.__get_by_id(employee_id)
        employee.is_active = not employee.is_active
        self.save()
        return employee.is_active

    def is_employee_active(self, employee_id: int) -> bool:
        if not employee_id:
            return False
        employee = self.__get_by_id(employee_id)
        return employee.is_active

    def get_therapist(self):
        return (self.db.session.query(Employee)
                .filter(or_(Employee.position == PositionEnum.PROFESOR_EQUITACION,
                            Employee.position == PositionEnum.TERAPEUTA))
                .all())

    def get_rider(self):
        return (self.db.session.query(Employee)
                .filter(or_(Employee.position == PositionEnum.CONDUCTOR))
                .all())

    def get_track_auxiliary(self):
        return (self.db.session.query(Employee)
                .filter(or_(Employee.position == PositionEnum.AUXILIAR_PISTA))
                .all())
