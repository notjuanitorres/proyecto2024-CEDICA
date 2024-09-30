from abc import abstractmethod
from typing import List, Dict
from src.core.module.equestrian.models import Horse
from src.core.database import db as database


class AbstractEquestrianRepository:

    @abstractmethod
    def add(self, horse: Horse) -> Horse:
        pass

    @abstractmethod
    def get_page(self, page: int, per_page: int, max_per_page: int, order_by: list):
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


class EquestrianRepository(AbstractEquestrianRepository):
    def __init__(self):
        self.db = database

    def add(self, horse: Horse):
        self.db.session.add(horse)
        self.db.session.flush()
        self.save()
        return horse

    def get_page(self, page: int, per_page: int, max_per_page: int, order_by: list):
        query = Horse.query
        if order_by:
            for field, direction in order_by:
                if direction == 'asc':
                    query = query.order_by(getattr(Horse, field).asc())
                elif direction == 'desc':
                    query = query.order_by(getattr(Horse, field).desc())

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
