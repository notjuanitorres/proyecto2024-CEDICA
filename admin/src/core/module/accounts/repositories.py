from abc import abstractmethod
from typing import List
from src.core.module.accounts.models import User


class AbstractAccountsRepository:

    @abstractmethod
    def create(self, **kwargs):
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
    def __init__(self, database):
        self.db = database

    def create(self, **kwargs):
        user = User(kwargs)
        self.save(user)

    def get_page(self, page: int, per_page: int, max_per_page: int):
        return User.query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, user_id: int):
        return self.db.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.session.query(User).filter(User.email == email).first()

    def update(self, user):
        pass

    # TODO: select between logic and physical erase
    def delete(self):
        pass

    def save(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def seed(self):
        self.create(email="example1@gmail.com", alias="Alias1", password="1234")
        self.create(email="example2@gmail.com", alias="Alias2", password="1234")
        self.create(email="example3@gmail.com", alias="Alias3", password="1234")
