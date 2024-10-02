from typing import Dict
from .models import Employee


class EmployeeMapper:
    @classmethod
    def from_entity(self, employee: "Employee") -> Dict:
        return {
            "id": employee.id,
            "name": employee.name,
            "lastname": employee.lastname,
            "phone_country_code": employee.country_code,
            "phone_area_code": employee.area_code,
            "phone_number": employee.phone,
            "dni": employee.dni,
            "profession": employee.profession.value,
            "position": employee.position.value,
            "job_condition": employee.job_condition.value,
            "start_date": employee.start_date,
            "end_date": employee.end_date,
            "is_active": employee.is_active,
            "street": employee.street,
            "number": employee.number,
            "department": employee.department,
            "locality": employee.locality,
            "province": employee.province,
            "emergency_contact_name": employee.emergency_contact_name,
            "emergency_contact_phone": employee.emergency_contact_phone,
            "health_insurance": employee.health_insurance,
            "affiliate_number": employee.affiliate_number,
            "email": employee.email,
            "user_id": employee.user_id,
            "inserted_at": employee.inserted_at,
            "updated_at": employee.updated_at,
        }

    @classmethod
    def to_entity(self, data: Dict) -> "Employee":
        return Employee(
            id=data.get("id"),
            name=data.get("name"),
            lastname=data.get("lastname"),
            country_code=data.get("phone_country_code"),
            area_code=data.get("phone_area_code"),
            phone=data.get("phone_number"),
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
        )

    @classmethod
    def from_form(self, data: Dict) -> "Dict":
        phone = data.get("phone", {})
        employment_information = data.get("employment_information", {})
        address = data.get("address", {})
        emergency_contact = data.get("emergency_contact", {})
        return {
            "id": data.get("id"),
            "name": data.get("first_name"),
            "lastname": data.get("last_name"),
            "country_code": phone.get("country_code"),
            "area_code": phone.get("area_code"),
            "phone": phone.get("number"),
            "dni": data.get("dni"),
            "profession": employment_information.get("profession"),
            "position": employment_information.get("position"),
            "job_condition": employment_information.get("job_condition"),
            "start_date": employment_information.get("start_date"),
            "end_date": employment_information.get("end_date"),
            "is_active": employment_information.get("is_active"),
            "street": address.get("street"),
            "number": address.get("number"),
            "department": address.get("department"),
            "locality": address.get("locality"),
            "province": address.get("province"),
            "emergency_contact_name": emergency_contact.get("emergency_contact_name"),
            "emergency_contact_phone": emergency_contact.get("emergency_contact_phone"),
            "health_insurance": data.get("health_insurance"),
            "affiliate_number": data.get("affiliate_number"),
            "email": data.get("email"),
            "user_id": data.get("user_id"),
        }

    @classmethod
    def to_form(self, data: Dict) -> "Dict":
        return {
            "first_name": data.get("name"),
            "last_name": data.get("lastname"),
            "dni": data.get("dni"),
            "phone": {
                "country_code": data.get("phone_country_code"),
                "area_code": data.get("phone_area_code"),
                "number": data.get("phone_number"),
            },
            "employment_information": {
                "profession": data.get("profession"),
                "position": data.get("position"),
                "job_condition": data.get("job_condition"),
                "start_date": data.get("start_date"),
                "end_date": data.get("end_date"),
                "is_active": data.get("is_active"),
            },
            "address": {
                "street": data.get("street"),
                "number": data.get("number"),
                "department": data.get("department"),
                "locality": data.get("locality"),
                "province": data.get("province"),
            },
            "emergency_contact": {
                "emergency_contact_name": data.get("emergency_contact_name"),
                "emergency_contact_phone": data.get("emergency_contact_phone"),
            },
            "health_insurance": data.get("health_insurance"),
            "affiliate_number": data.get("affiliate_number"),
            "email": data.get("email"),
            "user_id": data.get("user_id"),
        }

