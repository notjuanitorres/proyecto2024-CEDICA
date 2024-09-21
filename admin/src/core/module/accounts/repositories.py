from abc import abstractmethod
from typing import List
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
    def save(self, user):
        pass

    @abstractmethod
    def update(self, user):
        pass

    @abstractmethod
    def delete(self):
        pass


class AccountsRepository(AbstractAccountsRepository):
    def __init__(self):
        self.db = database

    def add(self, user: User):
        self.save(user)

    def get_page(self, page: int, per_page: int, max_per_page: int):
        return User.query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.session.query(User).filter(User.email == email).first()

    def update(self, user):
        pass

    # TODO: select between logic and physical erase
    def delete(self):
        pass

    def save(self, user):
        self.db.session.add(user)
        self.db.session.commit()
