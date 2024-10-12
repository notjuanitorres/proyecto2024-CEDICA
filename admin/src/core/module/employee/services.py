from abc import abstractmethod
from typing import Dict
from .repositories import AbstractEmployeeRepository
from .models import Employee
from .mappers import EmployeeMapper as Mapper


class AbstractEmployeeServices:
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
    def get_trainers(self):
        raise NotImplementedError

    @abstractmethod
    def search_by_email(self, email: str):
        raise NotImplementedError


class EmployeeServices(AbstractEmployeeServices):
    def __init__(self, employee_repository: AbstractEmployeeRepository):
        self.employee_repository = employee_repository

    def create_employee(self, employee: Dict) -> Dict | None:
        created_user = self.employee_repository.add(Mapper.to_entity(employee))

        return Mapper.from_entity(created_user)

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
        data["id"] = employee_id
        return self.employee_repository.update(employee_id, data)

    def delete_employee(self, employee_id: int) -> bool:
        pass

    def is_email_used(self, email: str) -> bool:
        employee = self.employee_repository.get_by_email(email=email)

        return employee is not None

    def is_dni_used(self, dni: str) -> bool:
        employee = self.employee_repository.get_by_dni(dni=dni)

        return employee is not None

    def get_trainers(self):
        return self.employee_repository.get_trainers()

    def search_by_email(self, email: str):
        return Employee.query.filter(Employee.email.icontains(email, autoescape=True)).all()

