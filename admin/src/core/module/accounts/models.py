from src.core.database import db
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    system_admin = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    role = db.relationship("Role", backref="users")


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'

    role_id = db.Column(db.BigInteger, db.ForeignKey(
        'roles.id'), primary_key=True)
    permission_id = db.Column(db.BigInteger, db.ForeignKey(
        'permissions.id'), primary_key=True)
    role = db.relationship('Role', backref=db.backref(
        'role_permissions', lazy=True))

    permission = db.relationship(
        'Permission', backref=db.backref('role_permissions', lazy=True))