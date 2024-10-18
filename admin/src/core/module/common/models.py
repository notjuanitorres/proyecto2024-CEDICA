from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr
from src.core.database import db


class File(db.Model):
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
    owner_type = db.Column(db.String)  # Polimorphic discriminator

    __mapper_args__ = {
        "polymorphic_on": owner_type,
    }

    def to_dict(self) -> dict:
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
    street = db.Column(db.String(50))
    number = db.Column(db.Integer)
    department = db.Column(db.String(50))
    locality = db.Column(db.String(50))
    province = db.Column(db.String(50))


@declarative_mixin
class EmergencyContactMixin:
    emergency_contact_name = db.Column(db.String(50))
    emergency_contact_phone = db.Column(db.String(20))


@declarative_mixin
class PhoneMixin:
    country_code = db.Column(db.String(5))
    area_code = db.Column(db.String(5))
    phone = db.Column(db.String(15))

    # @declared_attr
    # from sqlalchemy.orm import declared_attr
    # def phone_number(self):
    #     return db.column_property(self.country_code + self.area_code + self.phone)
