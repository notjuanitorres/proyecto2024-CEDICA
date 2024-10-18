from typing import Dict, List
from .models import JockeyAmazon, SchoolInstitution, FamilyMember, WorkAssignment, EducationLevelEnum, WorkConditionEnum, WorkProposalEnum, FamilyAssignmentEnum, DisabilityDiagnosisEnum, DisabilityTypeEnum, PensionEnum

class JockeyAmazonMapper:
    @classmethod
    def from_entity(cls, jockey: JockeyAmazon) -> Dict:
        return {
            "id": jockey.id,
            "first_name": jockey.first_name,
            "last_name": jockey.last_name,
            "dni": jockey.dni,
            "birth_date": jockey.birth_date,
            "birthplace": jockey.birthplace,
            "phone_country_code": jockey.country_code,
            "phone_area_code": jockey.area_code,
            "phone_number": jockey.phone,
            "street": jockey.street,
            "number": jockey.number,
            "department": jockey.department,
            "locality": jockey.locality,
            "province": jockey.province,
            "is_scholarship": jockey.is_scholarship,
            "scholarship_observations": jockey.scholarship_observations,
            "has_disability": jockey.has_disability,
            "disability_diagnosis": jockey.disability_diagnosis.value if jockey.disability_diagnosis else None,
            "disability_other": jockey.disability_other,
            "disability_type": jockey.disability_type.value if jockey.disability_type else None,
            "has_family_assignment": jockey.has_family_assignment,
            "family_assignment_type": jockey.family_assignment_type.value if jockey.family_assignment_type else None,
            "has_pension": jockey.has_pension.value if jockey.has_pension else None,
            "pension_details": jockey.pension_details,
            "social_security": jockey.social_security,
            "social_security_number": jockey.social_security_number,
            "has_curatorship": jockey.has_curatorship,
            "curatorship_observations": jockey.curatorship_observations,
            "school_institution_id": jockey.school_institution_id,
            "current_grade_year": jockey.current_grade_year,
            "school_observations": jockey.school_observations,
            "professionals": jockey.professionals,
            "inserted_at": jockey.inserted_at,
            "updated_at": jockey.updated_at,
            "emergency_contact": {
                "emergency_contact_name": jockey.emergency_contact_name,
                "emergency_contact_phone": jockey.emergency_contact_phone,
            },
            "family_members": [
                FamilyMemberMapper.from_entity(member) for member in jockey.family_members
            ],
            "work_assignment": WorkAssignmentMapper.from_entity(jockey.work_assignment)
        }

    @classmethod
    def to_entity(cls, data: Dict) -> JockeyAmazon:
        phone = data.get("phone", {})
        address = data.get("address", {})
        emergency_contact = data.get("emergency_contact", {})
        family_members = []

        if 'family_member1' in data:
            family_member1_data = data['family_member1']
            family_member1 = FamilyMemberMapper.to_entity(family_member1_data)
            family_members.append(family_member1)
        
        if 'family_member2' in data:
            family_member2_data = data['family_member2']
            if any(family_member2_data.values()):  # Check if family_member2 data is not empty
                family_member2 = FamilyMemberMapper.to_entity(family_member2_data)
                family_members.append(family_member2)

        return JockeyAmazon(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            dni=data.get("dni"),
            birth_date=data.get("birth_date"),
            birthplace=data.get("birthplace"),
            country_code=phone.get("country_code"),
            area_code=phone.get("area_code"),
            phone=phone.get("number"),
            street=address.get("street"),
            number=address.get("number"),
            department=address.get("department"),
            locality=address.get("locality"),
            province=address.get("province"),
            is_scholarship=data.get("is_scholarship"),
            scholarship_observations=data.get("scholarship_observations"),
            has_disability=data.get("has_disability"),
            disability_diagnosis=data.get("disability_diagnosis"),
            disability_other=data.get("disability_other"),
            disability_type=data.get("disability_type"),
            has_family_assignment=data.get("has_family_assignment"),
            family_assignment_type=data.get("family_assignment_type"),
            has_pension=data.get("has_pension"),
            pension_details=data.get("pension_details"),
            social_security=data.get("social_security"),
            social_security_number=data.get("social_security_number"),
            has_curatorship=data.get("has_curatorship"),
            curatorship_observations=data.get("curatorship_observations"),
            school_institution=SchoolInstitutionMapper.to_entity(data.get("school_institution")),
            school_institution_id=data.get("school_institution_id"),
            current_grade_year=data.get("current_grade_year"),
            school_observations=data.get("school_observations"),
            professionals=data.get("professionals"),
            inserted_at=data.get("inserted_at"),
            updated_at=data.get("updated_at"),
            emergency_contact_name=emergency_contact.get("emergency_contact_name"),
            emergency_contact_phone=emergency_contact.get("emergency_contact_phone"),
            family_members=family_members,
            work_assignment=WorkAssignmentMapper.to_entity(data.get("work_assignments"))
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
        return {
            "id": assignment.id,
            "proposal": assignment.proposal.value,
            "condition": assignment.condition.value,
            "sede": assignment.sede.value,
            "days": assignment.days.value,
            "professor_or_therapist_id": assignment.professor_or_therapist_id,
            "conductor_id": assignment.conductor_id,
            "track_assistant_id": assignment.track_assistant_id,
            "horse_id": assignment.horse_id,
        }

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
