from abc import abstractmethod
from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.pagination import Pagination
from src.core.database import db as database
from src.core.module.employee.models import Employee


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
        order_by: list,
        # search_params: Dict,
    ) -> Pagination:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, employee_id: int) -> Employee:
        raise NotImplementedError

    @abstractmethod
    def update(self, employee_id: int, data: Dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, employee_id: int) -> bool:
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
        order_by: List = None,
    ):
        query = Employee.query

        if order_by:
            for field, direction in order_by:
                if direction == "asc":
                    query = query.order_by(getattr(Employee, field).asc())
                elif direction == "desc":
                    query = query.order_by(getattr(Employee, field).desc())

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, employee_id: int) -> Employee:
        return (
            self.db.session.query(Employee).filter(Employee.id == employee_id).first()
        )

    def update(self, employee_id: int, data: Dict) -> bool:
        employee = Employee.query.filter_by(id=employee_id)
        if not employee:
            return False
        employee.update(data)

        self.save()
        return True

    def delete(self, employee_id: int) -> bool:
        pass
