from abc import abstractmethod
from typing import Dict
from .repositories import AbstractEmployeeRepository
from .models import Employee
from .mappers import EmployeeDTO


class AbstractEmployeeServices:
    @abstractmethod
    def create_employee(self, employee: EmployeeDTO) -> EmployeeDTO | None:
        raise NotImplementedError

    @abstractmethod
    def get_page(self, page: int, per_page: int, order_by: list):
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


class EmployeeServices(AbstractEmployeeServices):
    def __init__(self, employee_repository: AbstractEmployeeRepository):
        self.employee_repository = employee_repository

    def create_employee(self, employee: EmployeeDTO) -> EmployeeDTO | None:
        created_user = self.employee_repository.add(employee.to_entity())

        return EmployeeDTO.from_entity(created_user)

    def get_page(self, page: int, per_page: int, order_by: list):
        max_per_page = 100
        per_page = 20
        return self.employee_repository.get_page(page, per_page, max_per_page, order_by)

    def get_employee(self, employee_id: int) -> Dict | None:
        employee = self.employee_repository.get_by_id(employee_id)
        if not employee:
            return None
        return self.to_dict(employee)

    def update_employee(self, employee_id: int, data: Dict) -> None:
        pass

    def delete_employee(self, employee_id: int) -> bool:
        pass

    def to_dict(self, employee: Employee) -> Dict:
        employee_dict = {
            "id": employee.id,
            "email": employee.email,
            "phone": employee.phone,
            "name": employee.name,
            "lastname": employee.lastname,
            "fullname": employee.fullname,
            "dni": employee.dni,
            "profession": employee.profession.value,
            "position": employee.position.value,
            "job_condition": employee.job_condition.value,
            "start_date": employee.start_date,
            "end_date": employee.end_date,
            "health_insurance": employee.health_insurance,
            "affiliate_number": employee.affiliate_number,
            "is_active": employee.is_active,
            "inserted_at": employee.inserted_at,
            "updated_at": employee.updated_at,
            "user_id": employee.user_id,
        }
        return employee_dict
