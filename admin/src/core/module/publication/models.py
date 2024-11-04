from datetime import datetime
from sqlalchemy.orm import relationship
from src.core.database import db
from enum import Enum as pyEnum


class EstadoPublicacionEnum(pyEnum):
    """Enumeration for the different states of a publication.

    Attributes:
        DRAFT (str): The publication is a draft.
        PUBLISHED (str): The publication is published.
        ARCHIVED (str): The publication is archived.
    """
    DRAFT = "Borrador"
    PUBLISHED = "Publicado"
    ARCHIVED = "Archivado"


class Publication(db.Model):
    """
    Represents a publication entry that will be displayed on the application.

    Attributes:
        id (int): The publication identifier.
        publish_date (datetime): The date when the publication was published.
        creation_date (datetime): The date when the publication was created.
        update_date (datetime): The date when the publication was updated.
        title (str): The title of the publication.
        summary (str): The summary of the publication.
        content (str): The content of the publication.
        author_id (int): The identifier of the author of the publication.
        status (EstadoPublicacionEnum): The status of the publication.
        author (User): The author of the publication.
    """
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key=True)
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.Enum(EstadoPublicacionEnum), nullable=False, default=EstadoPublicacionEnum.DRAFT)

    # Relaciones
    author = relationship("User", backref=db.backref("publications", lazy=True))
