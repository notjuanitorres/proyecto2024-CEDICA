from abc import abstractmethod
from typing import Dict, List
from core.bcrypt import bcrypt
from src.core.module.user import AbstractUserRepository, UserMapper
from .repositories import AbstractAuthRepository
from .models import Role


class AbstractAuthServices:
    """
    Abstract base class for authentication services.

    This class defines the interface for authentication services, including methods
    for authenticating users, validating emails, retrieving roles and permissions,
    and checking user permissions.
    """

    @abstractmethod
    def authenticate(self, email: str, password: str) -> Dict | None:
        """
        Authenticate a user by their email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            Dict | None: The authenticated user data as a dictionary, or None if authentication fails.
        """
        pass

    @abstractmethod
    def validate_email(self, email: str) -> bool:
        """
        Validate if an email is already in use.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is in use, False otherwise.
        """
        pass

    @abstractmethod
    def get_role(self, role_id: int) -> Role:
        """
        Retrieve a role by its ID.

        Args:
            role_id (int): The ID of the role to retrieve.

        Returns:
            Role: The role with the specified ID.
        """
        pass

    @abstractmethod
    def get_roles(self) -> List[Role]:
        """
        Retrieve all roles.

        Returns:
            List[Role]: A list of all roles.
        """
        pass

    @abstractmethod
    def get_permissions_of(self, user_id: int) -> List[str]:
        """
        Retrieve the permissions associated with a user.

        Args:
            user_id (int): The ID of the user whose permissions are to be retrieved.

        Returns:
            List[str]: A list of permissions associated with the specified user.
        """
        pass

    @abstractmethod
    def has_permissions(self, user_id: int, permissions_required: List[str]) -> bool:
        """
        Check if a user has the required permissions.

        Args:
            user_id (int): The ID of the user to check.
            permissions_required (List[str]): A list of required permissions.

        Returns:
            bool: True if the user has the required permissions, False otherwise.
        """
        pass


class AuthServices(AbstractAuthServices):
    """
    Concrete implementation of the AbstractAuthServices.

    This class provides methods for authenticating users, validating emails, retrieving roles and permissions,
    and checking user permissions.
    """

    def __init__(
        self,
        auth_repository: AbstractAuthRepository,
        user_repository: AbstractUserRepository,
    ):
        """
        Initialize the AuthServices.

        Args:
            auth_repository (AbstractAuthRepository): The repository for authentication data.
            user_repository (AbstractUserRepository): The repository for user data.
        """
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    def validate_email(self, email: str) -> bool:
        """
        Validate if an email is already in use.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is in use, False otherwise.
        """
        email_exists = self.user_repository.get_by_email(email) is not None
        return email_exists

    def authenticate(self, email: str, password: str):
        """
        Authenticate a user by their email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            Dict | None: The authenticated user data as a dictionary, or None if authentication fails.
        """
        user = self.user_repository.get_by_email(email)
        if user is None or not user.enabled:
            return None
        password_match = bcrypt.check_password_hash(user.password, password)
        if not user.email == email or not password_match:
            return None
        return UserMapper.from_entity(user)

    def get_role(self, role_id: int) -> Role:
        """
        Retrieve a role by its ID.

        Args:
            role_id (int): The ID of the role to retrieve.

        Returns:
            Role: The role with the specified ID.
        """
        return self.auth_repository.get_role(role_id)

    def get_roles(self) -> List[Role]:
        """
        Retrieve all roles.

        Returns:
            List[Role]: A list of all roles.
        """
        return self.auth_repository.get_roles()

    def get_permissions_of(self, user_id: int) -> List[str]:
        """
        Retrieve the permissions associated with a user.

        Args:
            user_id (int): The ID of the user whose permissions are to be retrieved.

        Returns:
            List[str]: A list of permissions associated with the specified user.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return ["NO_PERMISSIONS"]
        permissions = self.auth_repository.get_permissions_of_role(user.role_id)
        return [permission.name for permission in permissions]

    def has_permissions(self, user_id: int, permissions_required: List[str]) -> bool:
        """
        Check if a user has the required permissions.

        Args:
            user_id (int): The ID of the user to check.
            permissions_required (List[str]): A list of required permissions.

        Returns:
            bool: True if the user has the required permissions, False otherwise.
        """
        if self.user_repository.is_sys_admin(user_id):
            return True
        if not self.user_repository.is_user_enabled(user_id):
            return False
        user_permissions = self.get_permissions_of(user_id)
        return any(permission in user_permissions for permission in permissions_required)
