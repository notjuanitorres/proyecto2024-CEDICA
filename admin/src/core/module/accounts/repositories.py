from abc import abstractmethod
from typing import List, Dict
from src.core.module.accounts.models import User
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
    def update(self, user_id: int, data: Dict):
        pass

    @abstractmethod
    def delete(self):
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
        updated_user = user.update(data)
        self.save()
        return updated_user

    # TODO: select between logic and physical erase
    def delete(self):
        pass

    def save(self):
        self.db.session.commit()
