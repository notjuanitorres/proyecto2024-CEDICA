from abc import abstractmethod
from typing import Dict, List
from .repositories import AbstractAccountsRepository
from src.core.module.accounts.models import User
from core.bcrypt import bcrypt


class AbstractAccountsServices:
    @abstractmethod
    def get_users(self, page: int = 1, per_page: int = 10) -> List[User]:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def create_user(self, data: Dict) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: int, data: Dict) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def authenticate(self, email: str, password: str) -> User:
        pass

    @abstractmethod
    def disable_user(self, user_id: int) -> User:
        pass


class AccountsServices(AbstractAccountsServices):
    def __init__(self, accounts_repository: AbstractAccountsRepository):
        self.accounts_repository = accounts_repository

    def get_users(self, page: int = 1, per_page: int = 10):
        pass

    def get_user(self, user_id: int):
        pass

    def get_user_by_email(self, email: str):
        return self.accounts_repository.get_by_email(email)

    def create_user(self, data: Dict):
        pass

    def update_user(self, user_id: int, data: Dict):
        pass

    def delete_user(self, user_id: int):
        pass

    def authenticate(self, email: str, password: str):
        user = self.get_user_by_email(email)

        if user is None:
            return None

        password_match = bcrypt.check_password_hash(user.password, password)

        if not user.email == email or not password_match:
            return None

        return user

    def disable_user(self, user_id: int) -> User:
        pass
