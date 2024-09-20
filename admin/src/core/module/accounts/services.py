from abc import abstractmethod
from typing import Dict, List
from core.bcrypt import bcrypt
from .repositories import AbstractAccountsRepository
from .models import User


class AbstractAccountsServices:

    @abstractmethod
    def create_user(self, data: Dict) -> User:
        pass

    @abstractmethod
    def get_page(self, page: int = 1, per_page: int = 10):
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: int, data: Dict) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass

    def register_user(self, user: User):
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

    def create_user(self, user: User):
        pass

    def get_page(self, page: int = 1, per_page: int = 10):
        max_per_page = 100
        return self.accounts_repository.get_page(page=page, per_page=per_page, max_per_page=max_per_page)

    def get_user(self, user_id: int):
        return self.accounts_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str):
        return self.accounts_repository.get_by_email(email)

    def register_user(self, user: User):
        pass

    def update_user(self, user_id: int, data: Dict):
        pass

    def delete_user(self, user_id: int):
        pass

    def authenticate(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)

        if user is None:
            return None

        password_match = bcrypt.check_password_hash(user.password, password)

        if not user.email == email or not password_match:
            return None

        return user

    def disable_user(self, user_id: int) -> User:
        pass
