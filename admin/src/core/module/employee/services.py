from abc import abstractmethod
from typing import Dict
from .repositories import AbstractEmployeeRepository
from .models import Employee, EmployeeFile
from .mappers import EmployeeMapper as Mapper


class AbstractEmployeeServices:
    def __init__(self):
        self.storage_path = "employees/"

    @abstractmethod
    def create_employee(self, employee: Dict) -> Dict | None:
        raise NotImplementedError

    @abstractmethod
    def get_page(self, page: int, per_page: int, search_query: Dict, order_by: list):
        raise NotImplementedError

    @abstractmethod
    def get_employee(self, employee_id: int) -> Dict | None:
        raise NotImplementedError

    @abstractmethod
    def update_employee(self, employee_id: int, data: Dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_employee(self, employee_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_email_used(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_dni_used(self, dni: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_document(self, employee_id: int, document: EmployeeFile) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_document(self, employee_id: int, document_id: int) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def delete_document(self, employee_id: int, document_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_trainers(self):
        raise NotImplementedError


class EmployeeServices(AbstractEmployeeServices):
    def __init__(
        self,
        employee_repository: AbstractEmployeeRepository,
    ):
        super().__init__()
        self.employee_repository = employee_repository

    def create_employee(self, employee: Employee) -> Dict | None:
        created_employee: Employee = self.employee_repository.add(employee)
        return Mapper.from_entity(created_employee)

    def get_page(self, page: int, per_page: int, search_query: Dict, order_by: list):
        max_per_page = 100
        per_page = 20
        return self.employee_repository.get_page(
            page, per_page, max_per_page, search_query, order_by
        )

    def get_employee(self, employee_id: int) -> Dict | None:
        employee = self.employee_repository.get_by_id(employee_id)
        if not employee:
            return None

        return Mapper.from_entity(employee)

    def update_employee(self, employee_id: int, data: Dict) -> None:
        return self.employee_repository.update(employee_id, data)

    def delete_employee(self, employee_id: int) -> bool:
        pass

    def is_email_used(self, email: str) -> bool:
        employee = self.employee_repository.get_by_email(email=email)
        return employee is not None

    def is_dni_used(self, dni: str) -> bool:
        employee = self.employee_repository.get_by_dni(dni=dni)
        return employee is not None

    def add_document(self, employee_id: int, document: EmployeeFile):
        return self.employee_repository.add_document(employee_id, document)

    def get_document(self, employee_id: int, document_id: int) -> Dict:
        return self.employee_repository.get_document(employee_id, document_id).to_dict()

    def delete_document(self, employee_id: int, document_id: int):
        return self.employee_repository.delete_document(employee_id, document_id)

    def get_trainers(self):
        return self.employee_repository.get_trainers()
