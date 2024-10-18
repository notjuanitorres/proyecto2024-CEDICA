from src.core.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    profile_image_url = db.Column(db.String, nullable=True) 
    system_admin = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    role = db.relationship("Role", backref="users")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.alias}, email={self.email})>"

    def to_dict(self) -> dict:
        user_dict = {
            "id": self.id,
            "email": self.email,
            "alias": self.alias,
            "enabled": self.enabled,
            "system_admin": self.system_admin,
            'role_id': self.role_id
        }
        return user_dict

