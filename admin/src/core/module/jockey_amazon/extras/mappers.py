from typing import Dict
from src.core.module.jockey_amazon.models import (
    SchoolInstitution,
    FamilyMember, WorkAssignment,
)


class FamilyMemberMapper:
    """
    Mapper class for converting between FamilyMember entities and dictionary representations.
    
    Provides bidirectional conversion between FamilyMember domain entities and their
    dictionary representations for data transfer and storage purposes.
    """

    @classmethod
    def from_entity(cls, member: FamilyMember) -> Dict:
        """
        Converts a FamilyMember entity to its dictionary representation.
        
        Args:
            member (FamilyMember): The family member entity to convert
            
        Returns:
            Dict: Dictionary containing all family member attributes, with keys:
                - id: Unique identifier
                - relationship: Relationship to the jockey
                - first_name: First name
                - last_name: Last name
                - dni: National identification number
                - street: Street address
                - number: Street number
                - department: Department/unit number (optional)
                - locality: City/locality
                - province: Province/state
                - phone_country_code: Country code for phone
                - phone_area_code: Area code for phone
                - phone_number: Phone number
                - email: Email address
                - education_level: Education level enum value
                - occupation: Current occupation
        """

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
            "education_level": member.education_level.name,
            "occupation": member.occupation,
        }

    @classmethod
    def to_entity(cls, data: Dict) -> FamilyMember:
        """
        Creates a FamilyMember entity from its dictionary representation.
        
        Args:
            data (Dict): Dictionary containing family member attributes
            
        Returns:
            FamilyMember: New FamilyMember entity instance
            
        Note:
            Missing dictionary values will result in None values in the entity
        """
        return FamilyMember(
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


class WorkAssignmentMapper:
    """
    Mapper class for converting between WorkAssignment entities and dictionary representations.
    
    Provides bidirectional conversion between WorkAssignment domain entities and their
    dictionary representations for data transfer and storage purposes. Handles special
    cases like empty assignments and enum conversions.
    """

    @classmethod
    def from_entity(cls, assignment: WorkAssignment) -> Dict:
        """
        Converts a WorkAssignment entity to its dictionary representation.
        
        Args:
            assignment (WorkAssignment): The work assignment entity to convert
            
        Returns:
            Dict: Dictionary containing work assignment attributes, with keys:
                - id: Unique identifier
                - proposal: Work proposal enum name
                - condition: Work condition enum name
                - sede: Location/headquarters enum name
                - days: List of day enum values
                - professor_or_therapist_id: ID of assigned professor/therapist
                - conductor_id: ID of assigned conductor
                - track_assistant_id: ID of assigned track assistant
                - horse_id: ID of assigned horse
                
        Note:
            Returns empty dictionary if assignment is None
            Enum values are converted to their string representations
        """

        dict = {}
        if assignment:
            dict = {
                "id": assignment.id,
                "proposal": assignment.proposal.name,
                "condition": assignment.condition.name,
                "sede": assignment.sede.name,
                "days": [day.value for day in assignment.days],
                "professor_or_therapist_id": assignment.professor_or_therapist_id,
                "conductor_id": assignment.conductor_id,
                "track_assistant_id": assignment.track_assistant_id,
                "horse_id": assignment.horse_id,
            }
        return dict

    @classmethod
    def to_entity(cls, data: Dict) -> WorkAssignment:
        """
        Creates a WorkAssignment entity from its dictionary representation.
        
        Args:
            data (Dict): Dictionary containing work assignment attributes
            
        Returns:
            WorkAssignment: New WorkAssignment entity instance
            
        Note:
            Missing dictionary values will result in None values in the entity
            String values are converted back to appropriate enum instances
        """

        return WorkAssignment(
            id=data.get("id"),
            proposal=data.get("proposal"),
            condition=data.get("condition"),
            sede=data.get("sede"),
            days=data.get("days"),
            professor_or_therapist_id=data.get("professor_or_therapist_id"),
            conductor_id=data.get("conductor_id"),
            track_assistant_id=data.get("track_assistant_id"),
            horse_id=data.get("horse_id"),
        )


class SchoolInstitutionMapper:
    """
    Mapper class for converting between SchoolInstitution entities and dictionary representations.
    
    Provides bidirectional conversion between SchoolInstitution domain entities and their
    dictionary representations for data transfer and storage purposes.
    """

    @classmethod
    def from_entity(cls, institution: SchoolInstitution) -> Dict:
        """
        Converts a SchoolInstitution entity to its dictionary representation.
        
        Args:
            institution (SchoolInstitution): The school institution entity to convert
            
        Returns:
            Dict: Dictionary containing school institution attributes, with keys:
                - id: Unique identifier
                - school_name: Name of the institution
                - street: Street address
                - number: Street number
                - department: Department/unit number (optional)
                - locality: City/locality
                - province: Province/state
                - phone_country_code: Country code for phone
                - phone_area_code: Area code for phone
                - phone_number: Phone number
                
        Note:
            The 'name' attribute is mapped to 'school_name' in the dictionary
        """

        return {
            "id": institution.id,
            "school_name": institution.name,
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
        """
        Creates a SchoolInstitution entity from its dictionary representation.
        
        Args:
            data (Dict): Dictionary containing school institution attributes
            
        Returns:
            SchoolInstitution: New SchoolInstitution entity instance
            
        Note:
            Missing dictionary values will result in None values in the entity
            The 'school_name' dictionary key is mapped to the 'name' entity attribute
        """
        
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
