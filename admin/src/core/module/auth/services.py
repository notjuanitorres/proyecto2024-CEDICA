from abc import abstractmethod
from typing import Dict, List
from core.bcrypt import bcrypt
from src.core.module.user import AbstractUserRepository, UserMapper
from .repositories import AbstractAuthRepository
from .models import Role


class AbstractAuthServices:
    @abstractmethod
    def authenticate(self, email: str, password: str) -> Dict | None:
        pass

    @abstractmethod
    def validate_email(self, email: str) -> bool:
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

    @abstractmethod
    def has_permissions(self, user_id: int, permissions_required: list[str]) -> bool:
        pass


class AuthServices(AbstractAuthServices):
    def __init__(
        self,
        auth_repository: AbstractAuthRepository,
        user_repository: AbstractUserRepository,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    def validate_email(self, email: str) -> bool:
        email_exists = self.user_repository.get_by_email(email) is not None
        return email_exists

    def authenticate(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)
        if user is None or not user.enabled:
            return None
        password_match = bcrypt.check_password_hash(user.password, password)
        if not user.email == email or not password_match:
            return None
        return UserMapper.from_entity(user)

    def get_role(self, role_id: int) -> Role:
        return self.auth_repository.get_role(role_id)

    def get_roles(self) -> List:
        return self.auth_repository.get_roles()

    def get_permissions_of(self, user_id: int) -> List:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return ["NO_PERMISSIONS"]
        permissions = self.auth_repository.get_permissions_of_role(user.role_id)
        return [permission.name for permission in permissions]

    def has_permissions(self, user_id: int, permissions_required: list[str]) -> bool:
        if self.user_repository.is_sys_admin(user_id):
            return True
        if not self.user_repository.is_user_enabled(user_id):
            return False
        user_permissions = self.get_permissions_of(user_id)
        return any(permission in user_permissions for permission in permissions_required)