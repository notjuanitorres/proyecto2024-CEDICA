from abc import abstractmethod
from typing import List, Dict
from src.core.database import db as database
from .models import Role, RolePermission, Permission


class AbstractAuthRepository:
    """
    Abstract base class for authentication repositories.

    This class defines the interface for authentication repositories, including methods
    for retrieving roles and permissions.
    """

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
    def get_permissions_of_role(self, role_id: int) -> List[Permission]:
        """
        Retrieve the permissions associated with a role.

        Args:
            role_id (int): The ID of the role whose permissions are to be retrieved.

        Returns:
            List[Permission]: A list of permissions associated with the specified role.
        """
        pass


class AuthRepository(AbstractAuthRepository):
    """
    Concrete implementation of the AbstractAuthRepository.

    This class provides methods for retrieving roles and permissions from the database.
    """

    def __init__(self):
        """
        Initialize the AuthRepository.
        """
        self.db = database

    def save(self):
        """
        Commit the current transaction to the database.

        Returns:
            None
        """
        self.db.session.commit()

    def get_role(self, role_id: int) -> Role:
        """
        Retrieve a role by its ID.

        Args:
            role_id (int): The ID of the role to retrieve.

        Returns:
            Role: The role with the specified ID.
        """
        return self.db.session.query(Role).filter(Role.id == role_id).first()

    def get_roles(self) -> List[Role]:
        """
        Retrieve all roles.

        Returns:
            List[Role]: A list of all roles.
        """
        return self.db.session.query(Role).all()

    def get_permissions_of_role(self, role_id: int) -> List[Permission]:
        """
        Retrieve the permissions associated with a role.

        Args:
            role_id (int): The ID of the role whose permissions are to be retrieved.

        Returns:
            List[Permission]: A list of permissions associated with the specified role.
        """
        permission_ids = RolePermission.query.filter(RolePermission.role_id == role_id).all()
        return (Permission.query.
                filter(Permission.id.in_([p.permission_id for p in permission_ids])).all())