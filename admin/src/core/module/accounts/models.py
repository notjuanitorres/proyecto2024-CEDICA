from src.core.database import db
from datetime import datetime

from enum import Enum as pyEnum


class RoleEnum(pyEnum):
    TECNICO = "Técnico"
    ECUESTRE = "Ecuestre"
    VOLUNTARIO = "Voluntario"
    ADMINISTRACION = "Administración"


class PermissionEnum(pyEnum):
    EQUIPO_INDEX = "equipo_index"
    EQUIPO_NEW = "equipo_new"
    EQUIPO_UPDATE = "equipo_update"
    EQUIPO_DESTROY = "equipo_destroy"
    EQUIPO_SHOW = "equipo_show"
    PAGOS_INDEX = "pagos_index"
    PAGOS_NEW = "pagos_new"
    PAGOS_UPDATE = "pagos_update"
    PAGOS_DESTROY = "pagos_destroy"
    PAGOS_SHOW = "pagos_show"
    JYA_INDEX = "jya_index"
    JYA_NEW = "jya_new"
    JYA_UPDATE = "jya_update"
    JYA_DESTROY = "jya_destroy"
    JYA_SHOW = "jya_show"
    COBROS_INDEX = "cobros_index"
    COBROS_NEW = "cobros_new"
    COBROS_UPDATE = "cobros_update"
    COBROS_DESTROY = "cobros_destroy"
    COBROS_SHOW = "cobros_show"
    ECUSTRE_INDEX = "ecuestre_index"
    ECUSTRE_NEW = "ecuestre_new"
    ECUSTRE_UPDATE = "ecuestre_update"
    ECUSTRE_DESTROY = "ecuestre_destroy"
    ECUSTRE_SHOW = "ecuestre_show"


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

    def __repr__(self):
        return f"<User(id={self.id}, username={self.alias}, email={self.email})>"


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
