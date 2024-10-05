from sqlalchemy.orm import declarative_mixin
from src.core.database import db


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
