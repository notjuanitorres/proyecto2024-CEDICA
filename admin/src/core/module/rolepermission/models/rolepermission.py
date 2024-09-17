from src.core.database import db

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    
    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.id'), primary_key=True)
    permission_id = db.Column(db.BigInteger, db.ForeignKey('permissions.id'), primary_key=True)
    
    role = db.relationship('Role', backref=db.backref('role_permissions', lazy=True))
    permission = db.relationship('Permission', backref=db.backref('role_permissions', lazy=True))
    
    def __repr__(self):
        return f'<RolePermission role_id={self.role_id} permission_id={self.permission_id}>'