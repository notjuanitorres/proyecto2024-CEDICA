from abc import abstractmethod
from typing import List, Dict
from src.core.database import db as database
from .models import Role, RolePermission, Permission


class AbstractAuthRepository:
    @abstractmethod
    def get_role(self, role_id: int) -> Role:
        pass

    @abstractmethod
    def get_roles(self) -> List[Role]:
        pass

    @abstractmethod
    def get_permissions_of_role(self, role_id: int) -> List:
        pass


class AuthRepository(AbstractAuthRepository):
    def __init__(self):
        self.db = database

    def save(self):
        self.db.session.commit()

    def get_role(self, role_id: int) -> Role:
        return self.db.session.query(Role).filter(Role.id == role_id).first()

    def get_roles(self) -> List[Role]:
        return self.db.session.query(Role).all()

    def get_permissions_of_role(self, role_id: int) -> List:
        permission_ids = RolePermission.query.filter(RolePermission.role_id == role_id).all()
        return (Permission.query.
                filter(Permission.id.in_([p.permission_id for p in permission_ids])).all())
