from typing import Dict
from .models import JockeyAmazon, SchoolInstitution, FamilyMember, EducationLevelEnum

class JockeyAmazonMapper:
    @classmethod
    def from_entity(cls, jockey: JockeyAmazon) -> Dict:
        return {
            "id": jockey.id,
            "first_name": jockey.first_name,
            "last_name": jockey.last_name,
            "dni": jockey.dni,
            "birth_date": jockey.birth_date,
            "gender": jockey.gender,
            "address": jockey.address,
            "phone": jockey.phone,
            "email": jockey.email,
            "work_condition": jockey.work_condition.value,
            "work_proposal": jockey.work_proposal.value,
            "family_assignment": jockey.family_assignment.value,
            "inserted_at": jockey.inserted_at,
            "updated_at": jockey.updated_at,
        }

    @classmethod
    def to_entity(cls, data: Dict) -> JockeyAmazon:
        return JockeyAmazon(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            dni=data.get("dni"),
            birth_date=data.get("birth_date"),
            gender=data.get("gender"),
            address=data.get("address"),
            phone=data.get("phone"),
            email=data.get("email"),
            work_condition=WorkConditionEnum(data.get("work_condition")),
            work_proposal=WorkProposalEnum(data.get("work_proposal")),
            family_assignment=FamilyAssignmentEnum(data.get("family_assignment")),
            inserted_at=data.get("inserted_at"),
            updated_at=data.get("updated_at"),
        )

class SchoolInstitutionMapper:
    @classmethod
    def from_entity(cls, institution: SchoolInstitution) -> Dict:
        return {
            "id": institution.id,
            "name": institution.name,
            "street": institution.street,
            "number": institution.number,
            "department": institution.department,
            "locality": institution.locality,
            "province": institution.province,
            "phone_country_code": institution.phone_country_code,
            "phone_area_code": institution.phone_area_code,
            "phone_number": institution.phone_number,
        }

    @classmethod
    def to_entity(cls, data: Dict) -> SchoolInstitution:
        return SchoolInstitution(
            id=data.get("id"),
            name=data.get("name"),
            street=data.get("street"),
            number=data.get("number"),
            department=data.get("department"),
            locality=data.get("locality"),
            province=data.get("province"),
            phone_country_code=data.get("phone_country_code"),
            phone_area_code=data.get("phone_area_code"),
            phone_number=data.get("phone_number"),
        )

class FamilyMemberMapper:
    @classmethod
    def from_entity(cls, member: FamilyMember) -> Dict:
        return {
            "id": member.id,
            "relationship": member.relationship,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "dni": member.dni,
            "street": member.street,
            "number": member.number,
            "department": member.department,
            "locality": member.locality,
            "province": member.province,
            "phone_country_code": member.phone_country_code,
            "phone_area_code": member.phone_area_code,
            "phone_number": member.phone_number,
            "email": member.email,
            "education_level": member.education_level.value,
            "occupation": member.occupation,
        }

    @classmethod
    def to_entity(cls, data: Dict) -> FamilyMember:
        return FamilyMember(
            id=data.get("id"),
            relationship=data.get("relationship"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            dni=data.get("dni"),
            street=data.get("street"),
            number=data.get("number"),
            department=data.get("department"),
            locality=data.get("locality"),
            province=data.get("province"),
            phone_country_code=data.get("phone_country_code"),
            phone_area_code=data.get("phone_area_code"),
            phone_number=data.get("phone_number"),
            email=data.get("email"),
            education_level=EducationLevelEnum(data.get("education_level")),
            occupation=data.get("occupation"),
        )