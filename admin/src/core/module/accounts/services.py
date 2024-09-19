from abc import abstractmethod
from typing import Dict
from .repositories import AbstractAccountsRepository


class AbstractAccountsServices:
    @abstractmethod
    def get_users(self, page: int = 1, per_page: int = 10):
        pass

    @abstractmethod
    def get_user(self, user_id: int):
        pass

    @abstractmethod
    def get_user_by_email(self, email: str):
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

    @abstractmethod
    def authenticate(self, email: str, password: str):
        pass


class AccountsServices(AbstractAccountsServices):
    def __init__(self, accounts_repository: AbstractAccountsRepository):
        self.accounts_repository = accounts_repository

    def get_users(self, page: int = 1, per_page: int = 10):
        pass

    def get_user(self, user_id: int):
        pass

    def get_user_by_email(self, email: str):
        pass

    def create_user(self, data: Dict):
        pass

    def update_user(self, user_id: int, data: Dict):
        pass

    def delete_user(self, user_id: int):
        pass

    def authenticate(self, email: str, password: str):
        pass
