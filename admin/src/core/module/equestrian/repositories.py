from abc import abstractmethod
from typing import List, Dict
from src.core.module.equestrian.models import Horse, HorseTrainers, JAEnum
# from src.core.module.members.models import Employee
from src.core.database import db as database
from sqlalchemy import inspect


def escape_like(string, escape_char='*'):
    """
    Escape the string parameter used in SQL LIKE expressions.

    ::

        from sqlalchemy_utils import escape_like


        query = session.query(User).filter(
            User.name.ilike(escape_like('John'))
        )


    :param string: a string to escape
    :param escape_char: escape character
    """
    return (
        string
        .replace(escape_char, escape_char * 2)
        .replace('%', escape_char + '%')
        .replace('_', escape_char + '_')
    )


class AbstractEquestrianRepository:

    @abstractmethod
    def add(self, horse: Horse) -> Horse:
        pass

    @abstractmethod
    def get_page(self, page: int, per_page: int, max_per_page: int, order_by: list, filters: Dict):
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

    def get_page(self, page: int, per_page: int, max_per_page: int, order_by: list, filters: Dict):
        query = Horse.query

        valid_columns = [column.key for column in inspect(Horse).columns]

        if filters['name']:
            query = query.filter(Horse.name.ilike(f"%{escape_like(filters['name'])}%"))

        if filters['ja_type']:
            try:
                ja_type = JAEnum[filters['ja_type']]
                query = query.filter(Horse.ja_type == ja_type)
            except KeyError:
                print("Invalid JA type")
                pass

        if order_by:
            for field, direction in order_by:
                if field in valid_columns:
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

    def get_trainers_of_horse(self, horse_id: int) -> List:
        # TODO: uncomment this when the Employee model is implemented

        horse_trainers = (self.db.session.query(HorseTrainers)
                          .filter(HorseTrainers.id_horse == horse_id).all())
        return [ht.id_trainer for ht in horse_trainers]

        # return (self.db.session.query(Employee)
        #         .filter(Employee.id.in_([ht.id_trainer for ht in horse_trainers])).all())

    def set_horse_trainers(self, horse_id: int, trainers_ids: List[int]):
        self.db.session.query(HorseTrainers).filter(HorseTrainers.id_horse == horse_id).delete()
        for trainer_id in trainers_ids:
            self.db.session.add(HorseTrainers(id_horse=horse_id, id_trainer=trainer_id))
        self.save()
