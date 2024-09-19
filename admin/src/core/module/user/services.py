from abc import abstractmethod
from typing import Dict
from .repositories import AbstractUserRepository


class AbstractUserServices:
    @abstractmethod
    def get_users(self, page: int = 1, per_page: int = 10):
        pass

    @abstractmethod
    def get_user(self, user_id: int):
        pass

    @abstractmethod
    def create_user(self, data: Dict):
        pass

    @abstractmethod
    def update_user(self, user_id: int, data: Dict):
        pass

    @abstractmethod
    def delete_user(self, user_id: int):
        pass


class UserServices(AbstractUserServices):
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    def get_users(self, page: int = 1, per_page: int = 10):
        pass

    def get_user(self, user_id: int):
        pass

    def create_user(self, data: Dict):
        pass

    def update_user(self, user_id: int, data: Dict):
        pass

    def delete_user(self, user_id: int):
        pass
