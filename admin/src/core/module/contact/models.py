import hashlib
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
    comment = db.Column(db.Text, nullable=True)
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


class Response(db.Model):
    """
    Represents a response to a message made by a portal visitor.
    """

    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    response_hash = db.Column(db.String, nullable=False)
    respond_to_message_id = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable=True)
    respond_to_message = db.relationship("Message", backref=db.backref("responses", lazy=True))
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        """
        Return a string representation of the Message object.

        Returns:
            str: A string representation of the Message object.
        """
        return f"<Message(id={self.id}, email={self.email})>"

    def __init__(self, respond_to_message_id=None, response_data=None):
        if response_data:
            self.response_hash = self.generate_sha256_hash(response_data)
        self.respond_to_message_id = respond_to_message_id

    def generate_sha256_hash(self, data):
        """
        Generate a SHA-256 hash of the given data.
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
