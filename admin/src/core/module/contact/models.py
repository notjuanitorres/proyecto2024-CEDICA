from datetime import datetime
from enum import Enum as pyEnum
from src.core.database import db

class MessageStateEnum(pyEnum):
    PENDING = "Pendiente"
    RESOLVED = "Resuelto"

class Message(db.Model):
    """
    Represents a message from a portal visitor.

    Attributes:

    """

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(MessageStateEnum), nullable=False)
    comment = db.Column(db.Text, nullable=True, default="")
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        """
        Return a string representation of the Message object.

        Returns:
            str: A string representation of the Message object.
        """
        return f"<Message(id={self.id}, email={self.email})>"
