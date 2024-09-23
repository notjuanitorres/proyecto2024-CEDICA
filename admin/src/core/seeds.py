from src.core.database import db
from src.core.module.accounts.models import User, Role, Permission, RolePermission


def seed_accounts():
    seed_roles()
    seed_permissions()
    seed_role_permissions()
    seed_users()

    db.session.commit()


def seed_roles():
    roles = [
        Role(name="admin"),
        Role(name="user")
    ]

    db.session.add_all(roles)


def seed_permissions():
    permissions = [
        Permission(name="prueba_roles")
    ]

    db.session.add_all(permissions)


def seed_role_permissions():
    role_permissions = [
        RolePermission(role_id=1, permission_id=1)
    ]

    db.session.add_all(role_permissions)


def seed_users():
    users = [
        User(email="falso1@gmail.com", alias="falso1", password="Falso123,", role_id=1),
        User(email="falso2@gmail.com", alias="falso2", password="Falso123,", role_id=1),
        User(email="falso3@gmail.com", alias="falso3", password="Falso123,", role_id=1)
        ]

    db.session.add_all(users)
