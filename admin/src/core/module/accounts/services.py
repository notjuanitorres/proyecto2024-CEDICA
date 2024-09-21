from abc import abstractmethod
from typing import Dict
from core.bcrypt import bcrypt
from .repositories import AbstractAccountsRepository
from .models import User


class AbstractAccountsServices:

    @abstractmethod
    def create_user(self, user_data: Dict) -> User | None:
        pass

    @abstractmethod
    def get_page(self, page: int = 1, per_page: int = 10):
        pass

    @abstractmethod
    def get_user(self, user_id: int):
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

    @abstractmethod
    def disable_user(self, user_id: int):
        pass


class AccountsServices(AbstractAccountsServices):
    def __init__(self, accounts_repository: AbstractAccountsRepository):
        self.accounts_repository = accounts_repository

    def create_user(self, user_data: Dict) -> User:
        email_exists = (
            self.accounts_repository.get_by_email(user_data["email"]) is not None
        )

        if email_exists:
            return None

        new_user = User(
            email=user_data["email"],
            alias=user_data["alias"],
            password=bcrypt.generate_password_hash(user_data["password"]),
            enabled=user_data["enabled"],
            system_admin=user_data["system_admin"],
            # role_id=user_data["role_id"],
        )
        return self.accounts_repository.add(new_user) 

    def get_page(self, page: int = 1, per_page: int = 10):
        max_per_page = 100
        return self.accounts_repository.get_page(
            page=page, per_page=per_page, max_per_page=max_per_page
        )

    def get_user(self, user_id: int):
        return self.accounts_repository.get_by_id(user_id)

    def update_user(self, user_id: int, data: Dict):
        pass

    def delete_user(self, user_id: int):
        pass

    def authenticate(self, email: str, password: str) -> User:
        user = self.accounts_repository.get_user_by_email(email)

        if user is None:
            return None

        password_match = bcrypt.check_password_hash(user.password, password)

        if not user.email == email or not password_match:
            return None

        return user

    def disable_user(self, user_id: int) -> User:
        pass
