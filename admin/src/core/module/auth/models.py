from src.core.database import db


class Role(db.Model):
    """
    Represents a role in the system.

    Attributes:
        id (int): The unique identifier for the role.
        name (str): The name of the role.
    """

    __tablename__ = 'roles'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class Permission(db.Model):
    """
    Represents a permission in the system.

    Attributes:
        id (int): The unique identifier for the permission.
        name (str): The name of the permission.
    """

    __tablename__ = 'permissions'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class RolePermission(db.Model):
    """
    Represents the association between roles and permissions.

    Attributes:
        role_id (int): The ID of the role.
        permission_id (int): The ID of the permission.
        role (Role): The role associated with the permission.
        permission (Permission): The permission associated with the role.
    """

    __tablename__ = 'role_permissions'

    role_id = db.Column(db.BigInteger, db.ForeignKey(
        'roles.id'), primary_key=True)
    permission_id = db.Column(db.BigInteger, db.ForeignKey(
        'permissions.id'), primary_key=True)
    role = db.relationship('Role', backref=db.backref(
        'role_permissions', lazy=True))
    permission = db.relationship(
        'Permission', backref=db.backref('role_permissions', lazy=True))
