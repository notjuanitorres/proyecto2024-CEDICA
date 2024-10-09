from abc import abstractmethod
from typing import List, Dict

from core.module.common.repositories import apply_filters
from src.core.module.equestrian.models import Horse, HorseTrainers
from src.core.database import db as database
from src.core.module.employee.models import Employee


class AbstractEquestrianRepository:

    @abstractmethod
    def add(self, horse: Horse) -> Horse:
        pass

    @abstractmethod
    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int,
            search_query: Dict = None,
            order_by: list = None,
    ):
        pass

    @abstractmethod
    def get_by_id(self, horse_id: int) -> Horse:
        pass

    @abstractmethod
    def update(self, horse_id: int, data: Dict) -> bool:
        pass

    @abstractmethod
    def delete(self, horse_id: int) -> bool:
        pass

    @abstractmethod
    def get_trainers_of_horse(self, horse_id: int) -> List:
        pass

    @abstractmethod
    def set_horse_trainers(self, horse_id: int, trainers_ids: List[int]):
        pass


class EquestrianRepository(AbstractEquestrianRepository):
    def __init__(self):
        self.db = database

    def add(self, horse: Horse):
        self.db.session.add(horse)
        self.db.session.flush()
        self.save()
        return horse

    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int,
            search_query: Dict = None,
            order_by: List = None,
    ):
        query = Horse.query

        query = apply_filters(Horse, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, horse_id: int) -> Horse | None:
        return self.db.session.query(Horse).filter(Horse.id == horse_id).first()

    def update(self, horse_id: int, data: Dict):
        horse = Horse.query.filter_by(id=horse_id)
        if not horse:
            return False
        horse.update(data)
        self.save()
        return True

    def delete(self, horse_id: int):
        horse = Horse.query.filter_by(id=horse_id)
        if not horse:
            return False
        horse.delete()
        self.save()
        return True

    def save(self):
        self.db.session.commit()

    def get_trainers_of_horse(self, horse_id: int) -> List:

        horse_trainers = (self.db.session.query(HorseTrainers)
                          .filter(HorseTrainers.id_horse == horse_id).all())

        return (self.db.session.query(Employee)
                .filter(Employee.id.in_([ht.id_employee for ht in horse_trainers])).all())

    def set_horse_trainers(self, horse_id: int, trainers_ids: List[int]):
        self.db.session.query(HorseTrainers).filter(HorseTrainers.id_horse == horse_id).delete()
        for trainer_id in trainers_ids:
            self.db.session.add(HorseTrainers(id_horse=horse_id, id_employee=trainer_id))
        self.save()
