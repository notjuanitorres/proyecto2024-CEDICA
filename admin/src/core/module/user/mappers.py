"""
mappers.py

This module defines the UserMapper class, which provides methods for converting
between user entities and data transfer objects (DTOs). It leverages bcrypt for
password hashing and includes methods for both creating and updating user entities.
"""

from typing import Dict
from src.core.bcrypt import bcrypt
from .models import User


class UserMapper:
    """
    A mapper class for converting between user entities and data transfer objects (DTOs).
    """

    @classmethod
    def to_entity(cls, user_data: Dict, is_creation: bool = True) -> User:
        """
        Convert a dictionary of user data to a User entity.

        Args:
            user_data (Dict): The dictionary containing user data.
            is_creation (bool): Flag indicating whether the operation is a creation or an update.

        Returns:
            User: The User entity created from the provided data.
        """
        if is_creation:
            hashed_password = bcrypt.generate_password_hash(user_data.get("password")).decode('utf-8')
        else:
            hashed_password = user_data.get("password")

        return User(
            email=user_data.get("email"),
            alias=user_data.get("alias"),
            password=hashed_password,
            enabled=user_data.get("enabled", True),
            system_admin=user_data.get("system_admin", False),
            role_id=user_data.get("role_id", None),
            is_deleted=user_data.get("is_deleted", False)
        )

    @classmethod
    def from_entity(cls, user: User) -> Dict:
        """
        Convert a User entity to a dictionary of user data.

        Args:
            user (User): The User entity to convert.

        Returns:
            Dict: A dictionary containing the user data.
        """
        return {
            "id": user.id,
            "email": user.email,
            "alias": user.alias,
            "enabled": user.enabled,
            "system_admin": user.system_admin,
            "role_id": user.role_id,
            "inserted_at": user.inserted_at,
            "updated_at": user.updated_at,
            "assigned_to": user.employee.id if user.employee else None,
            "is_deleted": user.is_deleted
        }