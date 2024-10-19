from typing import Dict
from src.core.module.jockey_amazon.models import (
    SchoolInstitution,
    FamilyMember, WorkAssignment,
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
            education_level=data.get("education_level"),
            occupation=data.get("occupation"),
        )

    @classmethod
    def from_form(cls, form) -> Dict:
        return {
            "relationship": form.relationship.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "dni": form.dni.data,
            "street": form.street.data,
            "number": form.number.data,
            "department": form.department.data,
            "locality": form.locality.data,
            "province": form.province.data,
            "phone_country_code": form.phone_country_code.data,
            "phone_area_code": form.phone_area_code.data,
            "phone_number": form.phone_number.data,
            "email": form.email.data,
            "education_level": form.education_level.data,
            "occupation": form.occupation.data,
        }

    @classmethod
    def to_form(cls, data: Dict, form):
        form.relationship.data = data.get("relationship")
        form.first_name.data = data.get("first_name")
        form.last_name.data = data.get("last_name")
        form.dni.data = data.get("dni")
        form.street.data = data.get("street")
        form.number.data = data.get("number")
        form.department.data = data.get("department")
        form.locality.data = data.get("locality")
        form.province.data = data.get("province")
        form.phone_country_code.data = data.get("phone_country_code")
        form.phone_area_code.data = data.get("phone_area_code")
        form.phone_number.data = data.get("phone_number")
        form.email.data = data.get("email")
        form.education_level.data = data.get("education_level")
        form.occupation.data = data.get("occupation")


class WorkAssignmentMapper:
    @classmethod
    def from_entity(cls, assignment: WorkAssignment) -> Dict:
        dict = {}
        if assignment:
            dict = {
                "id": assignment.id,
                "proposal": assignment.proposal.value,
                "condition": assignment.condition.value,
                "sede": assignment.sede.value,
                "days": [day.value for day in assignment.days],
                "professor_or_therapist_id": assignment.professor_or_therapist_id,
                "conductor_id": assignment.conductor_id,
                "track_assistant_id": assignment.track_assistant_id,
                "horse_id": assignment.horse_id,
            }
        return dict

    @classmethod
    def to_entity(cls, data: Dict) -> WorkAssignment:
        return WorkAssignment(
            id=data.get("id"),
            proposal=data.get("proposal"),
            condition=data.get("condition"),
            sede=data.get("sede"),
            days=[data.get("days")],
            professor_or_therapist_id=data.get("professor_or_therapist_id"),
            conductor_id=data.get("conductor_id"),
            track_assistant_id=data.get("track_assistant_id"),
            horse_id=data.get("horse_id"),
        )

    @classmethod
    def from_form(cls, form) -> Dict:
        return {
            "proposal": form.proposal.data,
            "condition": form.condition.data,
            "sede": form.sede.data,
            "days": form.days.data,
            "professor_or_therapist_id": form.professor_or_therapist_id.data,
            "conductor_id": form.conductor_id.data,
            "track_assistant_id": form.track_assistant_id.data,
            "horse_id": form.horse_id.data,
        }

    @classmethod
    def to_form(cls, data: Dict, form):
        form.proposal.data = data.get("proposal")
        form.condition.data = data.get("condition")
        form.sede.data = data.get("sede")
        form.days.data = data.get("days")
        form.professor_or_therapist_id.data = data.get("professor_or_therapist_id")
        form.conductor_id.data = data.get("conductor_id")
        form.track_assistant_id.data = data.get("track_assistant_id")
        form.horse_id.data = data.get("horse_id")


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
            name=data.get("school_name"),
            street=data.get("street"),
            number=data.get("number"),
            department=data.get("department"),
            locality=data.get("locality"),
            province=data.get("province"),
            phone_country_code=data.get("phone_country_code"),
            phone_area_code=data.get("phone_area_code"),
            phone_number=data.get("phone_number"),
        )
