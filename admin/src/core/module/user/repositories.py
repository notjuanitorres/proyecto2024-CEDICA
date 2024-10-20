from abc import abstractmethod
from typing import List, Dict
from src.core.database import db as database
from src.core.module.common.repositories import (
    apply_filters,
    apply_multiple_search_criteria,
)
from .models import User
from .mappers import UserMapper
from sqlalchemy import and_


class AbstractUserRepository:
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
    def get_active_users(self, page: int):
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Dict | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def update(self, user_id: int, data: Dict) -> None:
        pass

    @abstractmethod
    def archive(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def recover(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def toggle_activation(self, user_id: int) -> None:
        pass

    @abstractmethod
    def is_sys_admin(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def is_user_enabled(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def can_be_linked(self, email: str) -> int | None:
        pass


class UserRepository(AbstractUserRepository):
    def __init__(self):
        self.db = database

    def add(self, user: User):
        self.db.session.add(user)
        self.db.session.flush()
        self.save()

        return UserMapper.from_entity(user)

    def get_page(
        self,
        page: int = 1,
        per_page: int = 10,
        max_per_page: int = 30,
        search_query: Dict = None,
        order_by: List = None,
    ):
        query = User.query

        query = apply_filters(User, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_active_users(self, page: int = 1, search: str = ""):
        per_page = 7

        query = self.db.session.query(User).filter(
            and_(User.enabled == True, User.employee == None)
        )

        if search:
            search_fields = ["alias", "email"]
            query = apply_multiple_search_criteria(
                User, query, search_query={"text": search, "fields": search_fields}
            )

        return query.paginate(page=page, per_page=per_page, error_out=False)

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.session.query(User).filter(User.id == user_id).first()

    def get_user(self, user_id: int) -> Dict | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        return UserMapper.from_entity(user)

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
    
    def archive(self, user_id):
        user = User.query.get(user_id)
        if not user or user.system_admin or user.is_deleted:
            return False
        user.is_deleted = True
        user.enabled = False
        if user.employee:
            user.employee.user_id = None
        self.save()
        return True
    
    def recover(self, user_id):
        user = User.query.get(user_id)
        if not user or not user.is_deleted:
            return False
        user.is_deleted = False
        self.save()
        return True

    def toggle_activation(self, user_id: int) -> bool:
        if self.is_sys_admin(user_id):
            return False
        user = self.get_by_id(user_id)
        user.enabled = not user.enabled
        self.save()
        return True

    def is_sys_admin(self, user_id: int) -> bool:
        if not user_id:
            return False
        user = self.get_by_id(user_id)
        return user.system_admin

    def is_user_enabled(self, user_id: int) -> bool:
        if not user_id:
            return False
        user = self.get_by_id(user_id)
        return user.enabled

    def save(self):
        self.db.session.commit()

    def can_be_linked(self, email: str) -> int | None:
        user = self.get_by_email(email)
        # if user.is_deleted:
        #     return None
        if not user or user.employee:
            return None
        if user.email == email:
            return user.id

        return None
