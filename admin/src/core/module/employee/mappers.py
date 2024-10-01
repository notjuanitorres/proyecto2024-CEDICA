from typing import Optional, Dict
from datetime import datetime
from .models import Employee

class EmployeeDTO:
    def __init__(
        self,
        employee_id: Optional[int],
        first_name: Optional[str],
        last_name: Optional[str],
        phone_country_code: Optional[str],
        phone_area_code: Optional[str],
        phone_number: Optional[str],
        dni: Optional[str],
        profession: Optional[str],
        position: Optional[str],
        job_condition: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        is_active: Optional[bool],
        street: Optional[str],
        number: Optional[str],
        department: Optional[str],
        locality: Optional[str],
        province: Optional[str],
        emergency_contact_name: Optional[str],
        emergency_contact_phone: Optional[str],
        health_insurance: Optional[str],
        affiliate_number: Optional[str],
        email: Optional[str],
        user_id: Optional[int],
        inserted_at: Optional[datetime],
        updated_at: Optional[datetime],
    ):
        self.id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_country_code = phone_country_code
        self.phone_area_code = phone_area_code
        self.phone_number = phone_number
        self.dni = dni
        self.profession = profession
        self.position = position
        self.job_condition = job_condition
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.street = street
        self.number = number
        self.department = department
        self.locality = locality
        self.province = province
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.health_insurance = health_insurance
        self.affiliate_number = affiliate_number
        self.email = email
        self.user_id = user_id
        self.inserted_at = inserted_at
        self.updated_at = updated_at

    @classmethod
    def from_entity(cls, employee: "Employee") -> "EmployeeDTO":
        return cls(
            employee_id=employee.id,
            first_name=employee.name,
            last_name=employee.lastname,
            phone_country_code=employee.country_code,
            phone_area_code=employee.area_code,
            phone_number=employee.phone,
            dni=employee.dni,
            profession=employee.profession.value,
            position=employee.position.value,
            job_condition=employee.job_condition.value,
            start_date=employee.start_date,
            end_date=employee.end_date,
            is_active=employee.is_active,
            street=employee.street,
            number=employee.number,
            department=employee.department,
            locality=employee.locality,
            province=employee.province,
            emergency_contact_name=employee.emergency_contact_name,
            emergency_contact_phone=employee.emergency_contact_phone,
            health_insurance=employee.health_insurance,
            affiliate_number=employee.affiliate_number,
            email=employee.email,
            user_id=employee.user_id,
            inserted_at=employee.inserted_at,
            updated_at=employee.updated_at,
        )

    def to_entity(self) -> "Employee":
        return Employee(
            id=self.id,
            name=self.first_name,
            lastname=self.last_name,
            dni=self.dni,
            email=self.email,
            user_id=self.user_id,
            country_code=self.phone_country_code,
            area_code=self.phone_area_code,
            phone=self.phone_number,
            profession=self.profession,
            position=self.position,
            job_condition=self.job_condition,
            start_date=self.start_date,
            end_date=self.end_date,
            is_active=self.is_active,
            street=self.street,
            number=self.number,
            department=self.department,
            locality=self.locality,
            province=self.province,
            inserted_at=self.inserted_at,
            updated_at=self.updated_at,
            emergency_contact_name=self.emergency_contact_name,
            emergency_contact_phone=self.emergency_contact_phone,
            health_insurance=self.health_insurance,
            affiliate_number=self.affiliate_number,
        )

    @classmethod
    def from_dict(cls, data: Dict) -> "EmployeeDTO":
        return cls(
            employee_id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone_country_code=data.get("phone_country_code"),
            phone_area_code=data.get("phone_area_code"),
            phone_number=data.get("phone_number"),
            dni=data.get("dni"),
            profession=data.get("profession"),
            position=data.get("position"),
            job_condition=data.get("job_condition"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            is_active=data.get("is_active"),
            street=data.get("street"),
            number=data.get("number"),
            department=data.get("department"),
            locality=data.get("locality"),
            province=data.get("province"),
            emergency_contact_name=data.get("emergency_contact_name"),
            emergency_contact_phone=data.get("emergency_contact_phone"),
            health_insurance=data.get("health_insurance"),
            affiliate_number=data.get("affiliate_number"),
            email=data.get("email"),
            user_id=data.get("user_id"),
            inserted_at=data.get("inserted_at"),
            updated_at=data.get("updated_at"),
        )


    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_country_code": self.phone_country_code,
            "phone_area_code": self.phone_area_code,
            "phone_number": self.phone_number,
            "dni": self.dni,
            "profession": self.profession,
            "position": self.position,
            "job_condition": self.job_condition,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "street": self.street,
            "number": self.number,
            "department": self.department,
            "locality": self.locality,
            "province": self.province,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "health_insurance": self.health_insurance,
            "affiliate_number": self.affiliate_number,
            "email": self.email,
            "user_id": self.user_id,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_form(cls, data: Dict) -> "EmployeeDTO":
        basic_information = data.get("basic_information", {})
        phone = basic_information.get("phone", {})
        employment_information = data.get("employment_information", {})
        address = data.get("address", {})
        emergency_contact = data.get("emergency_contact", {})

        return cls(
            employee_id=data.get("id"),
            first_name=basic_information.get("first_name"),
            last_name=basic_information.get("last_name"),
            phone_country_code=phone.get("country_code"),
            phone_area_code=phone.get("area_code"),
            phone_number=phone.get("number"),
            dni=basic_information.get("dni"),
            profession=employment_information.get("profession"),
            position=employment_information.get("position"),
            job_condition=employment_information.get("job_condition"),
            start_date=employment_information.get("start_date"),
            end_date=employment_information.get("end_date"),
            is_active=employment_information.get("is_active"),
            street=address.get("street"),
            number=address.get("number"),
            department=address.get("department"),
            locality=address.get("locality"),
            province=address.get("province"),
            emergency_contact_name=emergency_contact.get("emergency_contact_name"),
            emergency_contact_phone=emergency_contact.get("emergency_contact_phone"),
            health_insurance=data.get("health_insurance"),
            affiliate_number=data.get("affiliate_number"),
            email=data.get("email"),
            user_id=data.get("user_id"),
            inserted_at=data.get("inserted_at"),
            updated_at=data.get("updated_at"),
        )

    def to_form(self) -> Dict:
        return {
            "basic_information": {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "dni": self.dni,
                "phone": {
                    "country_code": self.phone_country_code,
                    "area_code": self.phone_area_code,
                    "number": self.phone_number
                }
            },
            "employment_information": {
                "profession": self.profession,
                "position": self.position,
                "job_condition": self.job_condition,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "is_active": self.is_active
            },
            "address": {
                "street": self.street,
                "number": self.number,
                "department": self.department,
                "locality": self.locality,
                "province": self.province
            },
            "emergency_contact": {
                "emergency_contact_name": self.emergency_contact_name,
                "emergency_contact_phone": self.emergency_contact_phone
            },
            "health_insurance": self.health_insurance,
            "affiliate_number": self.affiliate_number,
            "email": self.email,
            "user_id": self.user_id,
        }