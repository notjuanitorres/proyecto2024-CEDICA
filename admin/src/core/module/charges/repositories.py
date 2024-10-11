from abc import abstractmethod
from typing import List, Dict

from src.core.database import db as database
from src.core.module.charges.models import Charge
from core.module.common.repositories import apply_filters


class AbstractChargeRepository:
    @abstractmethod
    def add(self, charge: Charge) -> Charge:
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
    def get_by_id(self, charge_id: int) -> Charge:
        pass

    @abstractmethod
    def update(self, charge_id: int, data: Dict) -> bool:
        pass

    @abstractmethod
    def delete(self, charge_id: int) -> bool:
        pass


class ChargeRepository(AbstractChargeRepository):
    def __init__(self):
        self.db = database

    def add(self, charge: Charge):
        self.db.session.add(charge)
        self.db.session.flush()
        self.save()
        return charge

    def get_page(
            self,
            page: int,
            per_page: int,
            search_query: Dict = None,
            order_by: List = None,
    ):
        max_per_page = 100

        query = Charge.query

        query = apply_filters(Charge, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, charge_id: int):
        return self.db.session.query(Charge).filter(Charge.id == charge_id).first()

    def update(self, charge_id: int, data: Dict):
        charge = self.get_by_id(charge_id)
        if not charge:
            return False
        charge.update(data)
        self.save()
        return True

    def delete(self, charge_id: int):
        charge = self.get_by_id(charge_id)
        if not charge:
            return False
        self.db.session.delete(charge)
        self.save()
        return True

    def save(self):
        self.db.session.commit()

