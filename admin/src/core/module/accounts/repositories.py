from abc import abstractmethod
from src.core.database import db
from src.core.module.accounts.models import User


class AbstractAccountsRepository:
    @abstractmethod
    def get_all(self, page: int = 1, per_page: int = 10):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class AccountsRepository(AbstractAccountsRepository):
    def __init__(self, database):
        self.db = database

    def get_all(self, page: int = 1, per_page: int = 10):
        pass

    def get_by_id(self, user_id: int):
        pass

    def get_by_email(self, email: str):
        return db.session.query(User).filter(User.email == email).first()

    def create(self, **kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()

    def update(self):
        pass

    def delete(self):
        pass

    def seed(self):
        self.create(email="example1@gmail.com", alias="Alias1", password="1234")
        self.create(email="example2@gmail.com", alias="Alias2", password="1234")
        self.create(email="example3@gmail.com", alias="Alias3", password="1234")
