from src.core.database import db
from flask_sqlalchemy import SQLAlchemy

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<Permission {self.name}>'