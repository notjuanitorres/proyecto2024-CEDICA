from src.core.database import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)


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
