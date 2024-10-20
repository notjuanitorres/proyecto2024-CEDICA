from abc import abstractmethod
from typing import List, Dict

from src.core.module.employee.models import Employee
from src.core.database import db as database
from src.core.module.charges.models import Charge
from src.core.module.common.repositories import apply_filters, apply_search_criteria
from .mappers import ChargeMapper as Mapper


class AbstractChargeRepository:
    @abstractmethod
    def add_charge(self, charge: Charge) -> Dict:
        pass

    @abstractmethod
    def get_page(
            self,
            page: int,
            per_page: int,
            search_query: Dict = None,
            order_by: list = None,
    ):
        pass

    @abstractmethod
    def get_by_id(self, charge_id: int) -> Dict | None:
        pass

    @abstractmethod
    def update_charge(self, charge_id: int, data: Dict) -> bool:
        pass

    @abstractmethod
    def delete_charge(self, charge_id: int) -> bool:
        pass

    @abstractmethod
    def archive_charge(self, charge_id) -> bool:
        raise NotImplementedError

    @abstractmethod
    def recover_charge(self, charge_id) -> bool:
        raise NotImplementedError


class ChargeRepository(AbstractChargeRepository):
    def __init__(self):
        self.db = database

    def add_charge(self, charge: Charge):
        self.db.session.add(charge)
        self.db.session.flush()
        self.save()
        return Mapper.from_entity(charge)

    def get_page(
            self,
            page: int,
            per_page: int,
            search_query: Dict = None,
            order_by: List = None,
    ):
        max_per_page = 100

        query = Charge.query

        # since name and lastname aren't in the Charge model, we need to apply the filters separately
        if search_query and "text" in search_query and "field" in search_query:
            employee_query = apply_search_criteria(Employee, Employee.query, search_query).all()
            employee_ids = [employee.id for employee in employee_query]
            query = query.filter(Charge.employee_id.in_(employee_ids))
            search_query.pop("text")
            search_query.pop("field")

        # apply_filters doesn't handle dates so we filter it here
        if "filters" in search_query and search_query["filters"]:
            if "start_date" in search_query["filters"] and "finish_date" in search_query["filters"]:
                query = (query
                         .filter(Charge.date_of_charge
                                 .between(search_query["filters"]["start_date"],
                                          search_query["filters"]["finish_date"])))
                search_query["filters"].pop("start_date")
                search_query["filters"].pop("finish_date")

        query = apply_filters(Charge, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def __get_by_id(self, charge_id: int):
        return Charge.query.get(charge_id)

    def get_by_id(self, charge_id: int) -> Dict | None:
        charge = self.db.session.query(Charge).filter(Charge.id == charge_id).first()
        return Mapper.from_entity(charge) if charge else None

    def update_charge(self, charge_id: int, data: Dict) -> bool:
        charge = Charge.query.filter_by(id=charge_id)
        if not charge:
            return False
        charge.update(data)
        self.save()
        return True

    def delete_charge(self, charge_id: int) -> bool:
        charge = self.__get_by_id(charge_id)
        if not charge:
            return False
        self.db.session.delete(charge)
        self.save()
        return True

    def archive_charge(self, charge_id) -> bool:
        charge = Charge.query.get(charge_id)
        if not charge or charge.is_archived:
            return False
        charge.is_archived = True
        self.save()
        return True

    def recover_charge(self, charge_id):
        charge = Charge.query.get(charge_id)
        if not charge or not charge.is_archived:
            return False
        charge.is_archived = False
        self.save()
        return True

    def save(self):
        self.db.session.commit()
