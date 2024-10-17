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
    def get_employee(self, employee_id: int) -> Dict:
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

    def __get_by_email(self, email: str) -> Employee | None:
        return self.db.session.query(Employee).filter(Employee.email == email).first()

    def __get_by_dni(self, dni: str) -> Employee | None:
        return self.db.session.query(Employee).filter(Employee.dni == dni).first()

    def __get_document(self, employee_id: int, document_id: int) -> EmployeeFile:
        document = (
            self.db.session.query(EmployeeFile)
            .filter_by(owner_id=employee_id, id=document_id)
            .first()
        )
        return document

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

    def get_employee(self, employee_id):
        return Mapper.from_entity(self.__get_by_id(employee_id))

    def update(self, employee_id: int, data: Dict) -> bool:
        employee = Employee.query.filter_by(id=employee_id)
        if not employee:
            return False
        employee.update(data)

        self.save()
        return True

    def delete(self, employee_id: int) -> bool:
        pass

    def is_email_used(self, email: str) -> bool:
        return self.__get_by_email(email) is not None

    def is_dni_used(self, dni: str) -> bool:
        return self.__get_by_dni(dni) is not None

    def add_document(self, employee_id: int, document: EmployeeFile):
        employee: Employee = self.__get_by_id(employee_id)
        employee.files.append(document)
        self.save()

    def get_document(self, employee_id: int, document_id: int) -> Dict:
        return self.__get_document(employee_id, document_id).to_dict()

    def delete_document(self, employee_id: int, document_id):
        employee: Employee = self.__get_by_id(employee_id)
        document = self.__get_document(employee.id, document_id)
        employee.files.remove(document)
        self.save()

    def get_trainers(self):
        return (
            self.db.session.query(Employee)
            .filter(
                or_(
                    Employee.position == PositionEnum["CONDUCTOR"],
                    Employee.position == PositionEnum["ENTRENADOR_CABALLOS"],
                )
            )
            .all()
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
