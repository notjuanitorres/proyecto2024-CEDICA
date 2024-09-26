from abc import abstractmethod
from typing import Dict, List
from core.bcrypt import bcrypt
from .repositories import AbstractAccountsRepository
from .models import User, Role


class AbstractAccountsServices:

    @abstractmethod
    def create_user(self, user_data: Dict) -> Dict | None:
        pass

    @abstractmethod
    def get_page(self, page: int, per_page: int):
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Dict | None:
        pass

    @abstractmethod
    def update_user(self, user_id: int, data: Dict) -> None:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def authenticate(self, email: str, password: str) -> Dict | None:
        pass

    @abstractmethod
    def disable_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def validate_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def is_sys_admin(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_role(self, role_id: int) -> Role:
        pass

    @abstractmethod
    def get_roles(self) -> List:
        pass

    @abstractmethod
    def get_permissions_of(self, user_id: int) -> List:
        pass


class AccountsServices(AbstractAccountsServices):
    def __init__(self, accounts_repository: AbstractAccountsRepository):
        self.accounts_repository = accounts_repository

    def validate_email(self, email: str) -> bool:
        email_exists = self.accounts_repository.get_by_email(email) is not None

        return email_exists

    def create_user(self, user_data: Dict):
        new_user = User(
            email=user_data.get("email"),
            alias=user_data.get("alias"),
            password=bcrypt.generate_password_hash(user_data.get("password")).decode('utf-8'),
            enabled=user_data.get("enabled", False),
            system_admin=user_data.get("system_admin", False),
            role_id=user_data.get("role_id", None),
        )
        return self.accounts_repository.add(new_user)

    def get_page(self, page: int, per_page: int):
        max_per_page = 100
        per_page = 20
        return self.accounts_repository.get_page(
            page=page, per_page=per_page, max_per_page=max_per_page
        )

    def get_user(self, user_id: int) -> Dict | None:
        user = self.accounts_repository.get_by_id(user_id)
        if not user:
            return None

        return self.to_dict(user)

    def update_user(self, user_id: int, data: Dict):
        return self.accounts_repository.update(user_id, data)

    def delete_user(self, user_id: int):
        return self.accounts_repository.delete(user_id)

    def authenticate(self, email: str, password: str):
        user = self.accounts_repository.get_by_email(email)

        if user is None or not user.enabled:
            return None

        password_match = bcrypt.check_password_hash(user.password, password)

        if not user.email == email or not password_match:
            return None

        return self.to_dict(user)

    def disable_user(self, user_id: int) -> User:
        pass

    def to_dict(self, user: User) -> Dict:
        # TODO: Implement User DTO to transfer users between service and presentation layer
        # The DTO is a dataclass with methods for passing from entity to dto and viceversa
        # It is possible to also add a to_dict method
        # It is easier to handle an object than a dict
        user_dict = {
            "id": user.id,
            "email": user.email,
            "alias": user.alias,
            "enabled": user.enabled,
            "system_admin": user.system_admin,
            'role_id': user.role_id
        }
        return user_dict

    def is_sys_admin(self, user_id: int) -> bool:
        if not user_id:
            return False
        user = self.accounts_repository.get_by_id(user_id)
        return user.system_admin

    def get_role(self, role_id: int) -> Role:
        return self.accounts_repository.get_role(role_id)

    def get_roles(self) -> List:
        return self.accounts_repository.get_roles()

    def get_permissions_of(self, user_id: int) -> List:
        user = self.accounts_repository.get_by_id(user_id)
        if not user:
            return ["NO_PERMISSIONS"]
        permissions = self.accounts_repository.get_permissions_of_role(user.role_id)
        return [p.name for p in permissions]
