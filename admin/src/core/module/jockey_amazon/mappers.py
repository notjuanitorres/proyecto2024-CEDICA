from typing import Dict
from .models import JockeyAmazon, JockeyAmazonFile
from .extras.mappers import (
    FamilyMemberMapper,
    WorkAssignmentMapper,
    SchoolInstitutionMapper,
)
from .forms import GeneralInformationForm, HealthInformationForm, FamilyInformationForm, SchoolInformationForm, WorkAssignmentsForm


class JockeyAmazonMapper:
    @classmethod
    def create_file(cls, document_type, file_information):
        horse_file = JockeyAmazonFile(
            path=file_information.get("path"),
            title=file_information.get("title"),
            is_link=file_information.get("is_link"),
            filetype=file_information.get("filetype"),
            filesize=file_information.get("filesize"),
            tag=document_type,
        )
        return horse_file

    @classmethod
    def create_files(cls, files):
        created_files = []
        for doc_type, files_info in files:
            for file_info in files_info:
                if file_info:
                    created_files.append(cls.create_file(doc_type, file_info))
        return created_files

    @classmethod
    def from_entity(cls, jockey: JockeyAmazon) -> Dict | None:
        jockey_dict = {
            "inserted_at": jockey.inserted_at,
            "updated_at": jockey.updated_at,
        }
        if jockey:
            jockey_dict["general_information"] = {
                "id": jockey.id,
                "first_name": jockey.first_name,
                "last_name": jockey.last_name,
                "dni": jockey.dni,
                "birth_date": jockey.birth_date,
                "birthplace": jockey.birthplace,
                "address": {
                    "street": jockey.street,
                    "number": jockey.number,
                    "department": jockey.department,
                    "locality": jockey.locality,
                    "province": jockey.province,
                },
                "emergency_contact": {
                    "emergency_contact_name": jockey.emergency_contact_name,
                    "emergency_contact_phone": jockey.emergency_contact_phone,
                },
                "phone": {
                    "country_code": jockey.country_code,
                    "area_code": jockey.area_code,
                    "number": jockey.phone,   
                }
            }
            jockey_dict["health_information"] = {
                "has_disability": jockey.has_disability,
                "disability_diagnosis": (
                    jockey.disability_diagnosis.name
                    if jockey.disability_diagnosis
                    else None
                ),
                "disability_other": jockey.disability_other,
                "disability_type": (
                    jockey.disability_type.name if jockey.disability_type else None
                ),
                "has_pension": jockey.has_pension,
                "pension_type": (
                    jockey.pension_type.name if jockey.pension_type else None
                ),
                "pension_details": jockey.pension_details,
                "social_security": jockey.social_security,
                "social_security_number": jockey.social_security_number,
                "has_curatorship": jockey.has_curatorship,
                "curatorship_observations": jockey.curatorship_observations,
            }
            jockey_dict["family_information"] = {
                "has_family_assignment": jockey.has_family_assignment,
                "family_assignment_type": (
                    jockey.family_assignment_type.value
                    if jockey.family_assignment_type
                    else None
                ),
                "family_members": [
                    FamilyMemberMapper.from_entity(member)
                    for member in jockey.family_members
                ],
            },
            jockey_dict["organization_work"] = {
                "professionals": jockey.professionals,
                "has_scholarship": jockey.has_scholarship,
                "scholarship_observations": jockey.scholarship_observations,
                "scholarship_percentage": jockey.scholarship_percentage,
                "work_assignments": WorkAssignmentMapper.from_entity(
                    jockey.work_assignment
                ),
            }
            jockey_dict["school_information"] = {
                "school_institution": SchoolInstitutionMapper.from_entity(jockey.school_institution),
                "school_institution_id": jockey.school_institution_id,
                "current_grade_year": jockey.current_grade_year,
                "school_observations": jockey.school_observations,
            }

            return jockey_dict

    @classmethod
    def to_entity(cls, data: Dict) -> JockeyAmazon:
        general = data.get("general_information", {})
        family = data.get("family_information", {})
        health = data.get("health_information", {})
        school = data.get("school_information", {})
        assignments = data.get("work_assignment_information", {})
        family_members = []

        # Handling family member 1
        if "family_member1" in data:
            family_member1_data = data["family_member1"]
            family_member1 = FamilyMemberMapper.to_entity(family_member1_data)
            family_members.append(family_member1)

        # Handling family member 2
        if "family_member2" in data:
            family_member2_data = data["family_member2"]
            if any(family_member2_data.values()):  # Check if family_member2 data is not empty
                family_member2 = FamilyMemberMapper.to_entity(family_member2_data)
                family_members.append(family_member2)

        # Return the entity with corrected mappings
        return JockeyAmazon(
            id=data.get("id"),

            # General Information
            first_name=general.get("first_name"),
            last_name=general.get("last_name"),
            dni=general.get("dni"),
            birth_date=general.get("birth_date"),
            birthplace=general.get("birthplace"),
            country_code=general.get("phone", {}).get("country_code"),
            area_code=general.get("phone", {}).get("area_code"),
            phone=general.get("phone", {}).get("number"),
            street=general.get("address", {}).get("street"),
            number=general.get("address", {}).get("number"),
            department=general.get("address", {}).get("department"),
            locality=general.get("address", {}).get("locality"),
            province=general.get("address", {}).get("province"),
            emergency_contact_name=general.get("emergency_contact", {}).get("emergency_contact_name"),
            emergency_contact_phone=general.get("emergency_contact", {}).get("emergency_contact_phone"),

            # Health Information 
            has_disability=health.get("has_disability"),
            disability_diagnosis=health.get("disability_diagnosis"),
            disability_other=health.get("disability_other"),
            disability_type=health.get("disability_type"),
            social_security=health.get("social_security"),
            social_security_number=health.get("social_security_number"),
            has_curatorship=health.get("has_curatorship"),
            curatorship_observations=health.get("curatorship_observations"),

            # School Information
            school_institution=SchoolInstitutionMapper.to_entity(school.get("school_institution", {})),
            school_institution_id=school.get("school_institution_id"),
            current_grade_year=school.get("current_grade_year"),
            school_observations=school.get("school_observations"),

            # Family Information
            has_family_assignment=family.get("has_family_assignment"),
            family_assignment_type=family.get("family_assignment_type"),
            family_members=family_members,

            # Work Assignments Information
            professionals=assignments.get("professionals"),
            work_assignment=WorkAssignmentMapper.to_entity(assignments.get("work_assignments")),
            has_scholarship=assignments.get("has_scholarship"),
            scholarship_observations=assignments.get("scholarship_observations"),
            scholarship_percentage=assignments.get("scholarship_percentage"),

            # Timestamps
            inserted_at=data.get("inserted_at"),
            updated_at=data.get("updated_at"),
        )
