from abc import abstractmethod
from typing import List, Dict
from src.core.module.accounts.models import User, Role, RolePermission, Permission
from src.core.database import db as database


class AbstractAccountsRepository:
    @abstractmethod
    def add(self, user: User) -> User | None:
        pass

    @abstractmethod
    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int,
            search_query: Dict = None,
            order_by: list = None,
    ):
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
    def toggle_activation(self, user_id: int) -> None:
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
        self.db.session.flush()
        self.save()
        
        return user

    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int,
            search_query: Dict = None,
            order_by: List = None,
    ):
        query = User.query

        if search_query:
            if "filters" in search_query and search_query["filters"]:
                for field, value in search_query["filters"].items():
                    if hasattr(User, field):
                        model_field = getattr(User, field)
                        query = query.filter(model_field == value)

            if "text" in search_query and "field" in search_query:
                if hasattr(User, search_query["field"]):
                    field = getattr(User, search_query["field"])
                    query = query.filter(field.ilike(f"%{search_query["text"]}%"))

        if order_by:
            for field, direction in order_by:
                if direction == "asc":
                    query = query.order_by(getattr(User, field).asc())
                elif direction == "desc":
                    query = query.order_by(getattr(User, field).desc())

        return query.paginate(
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

    def toggle_activation(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        user.enabled = not user.enabled
        self.save()

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
