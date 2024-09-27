from abc import abstractmethod
from typing import List, Dict
from src.core.module.accounts.models import User, Role, RolePermission, Permission
from src.core.database import db as database


class AbstractAccountsRepository:

    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_page(self, page: int, per_page: int, max_per_page: int) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def update(self, user_id: int, data: Dict) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_role(self, role_id: int) -> Role:
        pass

    @abstractmethod
    def get_roles(self) -> List[Role]:
        pass

    @abstractmethod
    def get_permissions_of_role(self, role_id: int) -> List:
        pass


class AccountsRepository(AbstractAccountsRepository):
    def __init__(self):
        self.db = database

    def add(self, user: User):
        self.db.session.add(user)
        self.save()

    def get_page(self, page: int, per_page: int, max_per_page: int):
        return User.query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.session.query(User).filter(User.email == email).first()

    def update(self, user_id: int, data: Dict):
        user = User.query.filter_by(id=user_id)
        if not user:
            return False
        user.update(data)
        self.save()
        return True

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        self.db.session.delete(user)
        self.save()
        return True

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
