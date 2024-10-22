from datetime import datetime
from enum import Enum

from sqlalchemy.orm import declarative_mixin
from src.core.database import db


class File(db.Model):
    """
    A database model representing a file entry in the system.

    Attributes:
        id (int): The unique identifier of the file.
        title (str): The title or name of the file.
        path (str): The file path or URL where the file is stored.
        is_link (bool): Indicates if the file is a URL link or an uploaded file.
        tag (str): An optional tag for categorizing or labeling the file.
        filetype (str): The type of the file (e.g., pdf, jpg, etc.).
        filesize (int): The size of the file in bytes.
        inserted_at (datetime): The timestamp when the file was uploaded.
        deleted (bool): Indicates if the file is marked as deleted.
        deleted_at (datetime, optional): The timestamp when the file was deleted.
        owner_type (str): A polymorphic discriminator to distinguish between
                          different types of owners (used for inheritance).

    """
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=100))
    path = db.Column(db.String(length=255))
    is_link = db.Column(db.Boolean, default=False)
    tag = db.Column(db.String(length=30))

    filetype = db.Column(db.String(length=25))
    filesize = db.Column(db.Integer)

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    owner_type = db.Column(db.String)  # Polymorphic discriminator

    __mapper_args__ = {
        "polymorphic_on": owner_type,
    }

    def to_dict(self) -> dict:
        """
        Converts the File object into a dictionary format.

        Returns:
            dict: A dictionary containing the file's attributes
        """
        return {
            "id": self.id,
            "path": self.path,
            "filetype": self.filetype,
            "filesize": self.filesize,
            "title": self.title,
            "tag": self.tag,
            "uploaded_at": self.inserted_at,
            "is_link": self.is_link,
        }


@declarative_mixin
class AddressMixin:
    """
    A mixin for adding address-related fields to a model.

    Attributes:
        street (str): The street name of the address.
        number (int): The building number.
        department (str): The department or unit number (optional).
        locality (str): The city or locality.
        province (str): The province or state.
    """
    street = db.Column(db.String(50))
    number = db.Column(db.Integer)
    department = db.Column(db.String(50))
    locality = db.Column(db.String(50))
    province = db.Column(db.String(50))


@declarative_mixin
class EmergencyContactMixin:
    """
    A mixin for adding emergency contact fields to a model.

    Attributes:
        emergency_contact_name (str): The name of the emergency contact.
        emergency_contact_phone (str): The phone number of the emergency contact.
    """
    emergency_contact_name = db.Column(db.String(50))
    emergency_contact_phone = db.Column(db.String(20))


@declarative_mixin
class PhoneMixin:
    """
    A mixin for adding phone-related fields to a model.

    Attributes:
        country_code (str): The country code for the phone number.
        area_code (str): The area code for the phone number.
        phone (str): The local phone number.
    """
    country_code = db.Column(db.String(5))
    area_code = db.Column(db.String(5))
    phone = db.Column(db.String(15))


class ArgentinaProvincies(Enum):
    """Enum with Argentina's provinces."""
    BUENOS_AIRES = "Buenos Aires"
    CABA = "Ciudad Autónoma de Buenos Aires"
    CATAMARCA = "Catamarca"
    CHACO = "Chaco"
    CHUBUT = "Chubut"
    CORDOBA = "Córdoba"
    CORRIENTES = "Corrientes"
    ENTRE_RIOS = "Entre Ríos"
    FORMOSA = "Formosa"
    ISLAS_MALVINAS = "Islas Malvinas"
    JUJUY = "Jujuy"
    LA_PAMPA = "La Pampa"
    LA_RIOJA = "La Rioja"
    MENDOZA = "Mendoza"
    MISIONES = "Misiones"
    NEUQUEN = "Neuquén"
    RIO_NEGRO = "Río Negro"
    SALTA = "Salta"
    SAN_JUAN = "San Juan"
    SAN_LUIS = "San Luis"
    SANTA_CRUZ = "Santa Cruz"
    SANTA_FE = "Santa Fe"
    SANTIAGO_DEL_ESTERO = "Santiago del Estero"
    TIERRA_DEL_FUEGO = "Tierra del Fuego"
    TUCUMAN = "Tucumán"
