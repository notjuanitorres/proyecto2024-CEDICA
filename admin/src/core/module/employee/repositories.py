from abc import abstractmethod
from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.pagination import Pagination
from src.core.database import db as database
from src.core.module.employee.models import Employee, EmployeeFile
from src.core.module.common.repositories import apply_filters
from src.core.module.employee.data import JobPositionEnum as PositionEnum
from sqlalchemy import or_


class AbstractEmployeeRepository:
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
    def get_by_id(self, employee_id: int) -> Employee:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Employee:
        raise NotImplementedError

    def get_by_dni(self, dni: str) -> Employee:
        raise NotImplementedError

    @abstractmethod
    def update(self, employee_id: int, data: Dict) -> bool:
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
    def get_trainers(self) -> List:
        raise NotImplementedError


class EmployeeRepository(AbstractEmployeeRepository):
    def __init__(self):
        self.db: SQLAlchemy = database

    def save(self):
        self.db.session.commit()

    def add(self, employee: Employee):
        self.db.session.add(employee)
        self.db.session.flush()
        self.save()

        return employee

    def get_page(
        self,
        page: int,
        per_page: int,
        max_per_page: int,
        search_query: Dict = None,
        order_by: List = None,
    ):
        query = Employee.query

        query = apply_filters(Employee, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, employee_id: int) -> Employee:
        return (
            self.db.session.query(Employee).filter(Employee.id == employee_id).first()
        )

    def get_by_email(self, email: str) -> Employee | None:
        return self.db.session.query(Employee).filter(Employee.email == email).first()

    def get_by_dni(self, dni: str) -> Employee | None:
        return self.db.session.query(Employee).filter(Employee.dni == dni).first()

    def update(self, employee_id: int, data: Dict) -> bool:
        employee = Employee.query.filter_by(id=employee_id)
        if not employee:
            return False
        employee.update(data)

        self.save()
        return True

    def add_document(self, employee_id: int, documents):
        employee: Employee = self.get_by_id(employee_id)
        employee.files.append(documents)
        self.save()

    def get_document(self, employee_id: int, document_id: int):
        document = (
            self.db.session.query(EmployeeFile)
            .filter_by(owner_id=employee_id, id=document_id)
            .first()
        )

        return document

    def delete_document(self, employee_id: int, document_id):
        employee: Employee = self.get_by_id(employee_id)
        document = self.get_document(employee.id, document_id)
        employee.files.remove(document)
        self.save()

    def delete(self, employee_id: int) -> bool:
        pass

    def get_trainers(self):
        return (self.db.session.query(Employee)
                .filter(or_(Employee.position == PositionEnum["CONDUCTOR"],
                        Employee.position == PositionEnum["ENTRENADOR_CABALLOS"]))
                .all())
