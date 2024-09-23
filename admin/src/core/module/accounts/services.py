from abc import abstractmethod
from typing import Dict
from core.bcrypt import bcrypt
from .repositories import AbstractAccountsRepository
from .models import User


class AbstractAccountsServices:

    @abstractmethod
    def create_user(self, user_data: Dict) -> Dict | None:
        pass

    @abstractmethod
    def get_page(self, page: int = 1, per_page: int = 10):
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Dict:
        pass

    @abstractmethod
    def update_user(self, user_id: int, data: Dict) -> None:
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

    @abstractmethod
    def validate_email(self, email: str) -> bool:
        pass


class AccountsServices(AbstractAccountsServices):
    def __init__(self, accounts_repository: AbstractAccountsRepository):
        self.accounts_repository = accounts_repository

    def validate_email(self, email: str) -> bool:
        email_exists = self.accounts_repository.get_by_email(email) is not None
        
        return email_exists

    def create_user(self, user_data: Dict):
        new_user = User(
            email=user_data["email"],
            alias=user_data["alias"],
            password=bcrypt.generate_password_hash(user_data["password"]).decode('utf-8'),
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

    def get_user(self, user_id: int) -> Dict | None:
        user = self.accounts_repository.get_by_id(user_id)
        if not user:
            return None
        
        return self.to_dict(user)

    def update_user(self, user_id: int, data: Dict):
        return self.accounts_repository.update(user_id, data)
        

    def delete_user(self, user_id: int):
        pass

    def authenticate(self, email: str, password: str):
        user = self.accounts_repository.get_by_email(email)

        if user is None:
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
            # TODO: Insert roles and permissions into the db
            # 'role_id':create_form.role_id.data,
        }
        return user_dict
