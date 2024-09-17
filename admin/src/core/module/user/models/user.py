from src.core.database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    system_admin = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    inserted_at = db.Column(db.DatetTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    role = db.relationship("Role", back_populates="users")

    def __repr__(self):
        return f'<User {self.email}>'
