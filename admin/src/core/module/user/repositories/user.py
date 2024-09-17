from src.core.database import db
from src.core.module.user.models.user import User


def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()


def list_user():
    return User.query.all()


def seed():
    create_user(email="example1@gmail.com", alias="Alias1", password="1234")
    create_user(email="example2@gmail.com", alias="Alias2", password="1234")
    create_user(email="example3@gmail.com", alias="Alias3", password="1234")
