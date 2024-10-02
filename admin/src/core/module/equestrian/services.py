from abc import abstractmethod
from typing import Dict, List
from .repositories import AbstractEquestrianRepository
from .models import Horse


class AbstractEquestrianServices:
    @abstractmethod
    def create_horse(self, horse_data: Dict) -> Horse | None:
        pass

    @abstractmethod
    def get_page(self, page: int, per_page: int, order_by: list, filters: Dict):
        pass

    @abstractmethod
    def get_horse(self, horse_id: int) -> Dict | None:
        pass

    @abstractmethod
    def update_horse(self, horse_id: int, data: Dict) -> bool:
        pass

    @abstractmethod
    def delete_horse(self, horse_id: int) -> bool:
        pass

    @abstractmethod
    def set_horse_trainers(self, horse_id: int, trainers_ids: List[int]):
        pass

    @abstractmethod
    def get_trainers_of_horse(self, horse_id: int) -> List:
        pass


class EquestrianServices(AbstractEquestrianServices):
    def __init__(self, equestrian_repository: AbstractEquestrianRepository):
        self.equestrian_repository = equestrian_repository

    def create_horse(self, horse_data: Dict):
        new_horse = Horse(
            name=horse_data.get("name"),
            breed=horse_data.get("breed"),
            birth_date=horse_data.get("birth_date"),
            coat=horse_data.get("coat"),
            is_donation=horse_data.get("is_donation"),
            admission_date=horse_data.get("admission_date"),
            assigned_facility=horse_data.get("assigned_facility"),
            ja_type=horse_data.get("ja_type"),
            sex=horse_data.get("sex")
        )
        created_horse = self.equestrian_repository.add(new_horse)

        return self.to_dict(created_horse)

    def get_page(self, page: int, per_page: int, order_by: list, filters: Dict):
        max_per_page = 100
        per_page = 20
        return self.equestrian_repository.get_page(page, per_page, max_per_page, order_by, filters)

    def get_horse(self, horse_id: int):
        horse = self.equestrian_repository.get_by_id(horse_id)
        if not horse:
            return None
        return self.to_dict(horse)

    def update_horse(self, horse_id: int, data: Dict):
        return self.equestrian_repository.update(horse_id, data)

    def delete_horse(self, horse_id: int):
        return self.equestrian_repository.delete(horse_id)

    def to_dict(self, horse: Horse):
        # TODO: Implement Horse DTO to transfer users between service and presentation layer
        return {
            "id": horse.id,
            "name": horse.name,
            "breed": horse.breed,
            "birth_date": horse.birth_date,
            "coat": horse.coat,
            "is_donation": horse.is_donation,
            "admission_date": horse.admission_date,
            "assigned_facility": horse.assigned_facility,
            "ja_type": horse.ja_type,
            "inserted_at": horse.inserted_at,
            "updated_at": horse.updated_at,
            "sex": horse.sex
        }

    def set_horse_trainers(self, horse_id: int, trainers_ids: List[int]):
        self.equestrian_repository.set_horse_trainers(horse_id, trainers_ids)

    def get_trainers_of_horse(self, horse_id: int) -> List:
        return self.equestrian_repository.get_trainers_of_horse(horse_id)
