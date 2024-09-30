from typing import Optional, Dict
from datetime import datetime, date
from .models import Employee, ProfessionsEnum, PositionEnum, ConditionEnum


class EmployeeDTO:
    def __init__(
        self,
        employee_id: Optional[int],
        basic_information: Dict,
        employment_information: Dict,
        address: Dict,
        emergency_contact: Dict,
        health_insurance: Optional[str],
        affiliate_number: Optional[str],
        email: Optional[str],
        user_id: Optional[int],
        inserted_at: Optional[datetime],
        updated_at: Optional[datetime],
    ):
        self.id = employee_id
        self.basic_information = basic_information
        self.employment_information = employment_information
        self.address = address
        self.emergency_contact = emergency_contact
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
            basic_information={
                "first_name": employee.name,
                "last_name": employee.lastname,
                "phone": {
                    "country_code": employee.country_code,
                    "area_code": employee.area_code,
                    "number": employee.phone,
                },
                "dni": employee.dni,
            },
            employment_information={
                "profession": employee.profession.value,
                "position": employee.position.value,
                "job_condition": employee.job_condition.value,
                "start_date": employee.start_date,
                "end_date": employee.end_date,
                "is_active": employee.is_active,
            },
            address={
                "street": employee.street,
                "number": employee.number,
                "department": employee.department,
                "locality": employee.locality,
                "province": employee.province,
            },
            emergency_contact={
                "emergency_contact_name": employee.emergency_contact_name,
                "emergency_contact_phone": employee.emergency_contact_phone,
            },
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
            name=self.basic_information.get("first_name"),
            lastname=self.basic_information.get("last_name"),
            dni=self.basic_information.get("dni"),
            email=self.email,
            user_id=self.user_id,
            country_code=self.basic_information.get("phone").get("country_code"),
            area_code=self.basic_information.get("phone").get("area_code"),
            phone=self.basic_information.get("phone").get("number"),
            profession=self.employment_information.get("profession"),
            position=self.employment_information.get("position"),
            job_condition=self.employment_information.get("job_condition"),
            start_date=self.employment_information.get("start_date"),
            end_date=self.employment_information.get("end_date"),
            is_active=self.employment_information.get("is_active"),
            street=self.address.get("street"),
            number=self.address.get("number"),
            department=self.address.get("department"),
            locality=self.address.get("locality"),
            province=self.address.get("province"),
            inserted_at=self.inserted_at,
            updated_at=self.updated_at,
            emergency_contact_name=self.emergency_contact.get("emergency_contact_name"),
            emergency_contact_phone=self.emergency_contact.get(
                "emergency_contact_phone"
            ),
            health_insurance=self.health_insurance,
            affiliate_number=(
                int(self.affiliate_number)
                if self.affiliate_number is not None
                else None
            ),
        )

    @classmethod
    def from_dict(cls, data: Dict) -> "EmployeeDTO":
        return cls(
            employee_id=data.get("id"),
            basic_information=data.get("basic_information"),
            employment_information=data.get("employment_information"),
            address=data.get("address"),
            emergency_contact=data.get("emergency_contact"),
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
            "basic_information": self.basic_information,
            "employment_information": self.employment_information,
            "address": self.address,
            "emergency_contact": self.emergency_contact,
            "health_insurance": self.health_insurance,
            "affiliate_number": self.affiliate_number,
            "email": self.email,
            "user_id": self.user_id,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
        }
