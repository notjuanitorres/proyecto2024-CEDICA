from typing import Dict
from src.core.bcrypt import bcrypt
from .models import User

class UserMapper:
    @classmethod
    def to_entity(self, user_data: Dict, is_creation: bool = True) -> User:
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
        )
    @classmethod
    def from_entity(self, user: User) -> "Dict":
        return {
            "id": user.id,
            "email": user.email,
            "alias": user.alias,
            "enabled": user.enabled,
            "system_admin": user.system_admin,
            "role_id": user.role_id,
            "inserted_at": user.inserted_at,
            "updated_at": user.updated_at,
            "assigned_to": user.employee.id if user.employee else None
        }