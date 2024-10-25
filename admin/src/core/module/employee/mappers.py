"""
This module defines a mapper class for the employee entities.
It controls the instantiation and serialization of an employee.
"""

from typing import Dict
from .models import Employee, EmployeeFile


class EmployeeMapper:
    """
    A mapper class for handling the transformation between 
    Employee entities and their corresponding data structures.

    This class is responsible for creating, serializing, and deserializing
    Employee objects and their associated files. It provides methods to
    instantiate Employee entities from raw input data and to convert 
    Employee entities back into dictionaries for easier processing 
    and storage.

    Methods:
        create_file(document_type, file_information): 
            Creates an EmployeeFile instance from provided file information.
        
        create_files(files): 
            Creates a list of EmployeeFile instances from a list of file information.
        
        to_entity(data, files): 
            Converts a dictionary into an Employee entity.
        
        from_entity(employee, documents=True): 
            Converts an Employee entity into a dictionary representation.
        
        flat_form(data): 
            Converts structured form data into a flat representation.
    """
    @classmethod
    def create_file(cls, document_type, file_information):
        """
        Create an EmployeeFile polymorphic instance of File from
        uploaded file information.

        Args:
            document_type (str): The type of the document.
            file_information (dict): The information of the file.

        Returns:
            EmployeeFile: The created Employee instance.
        """
        employee_file = EmployeeFile(
            path=file_information.get("path"),
            title=file_information.get("title"),
            is_link=file_information.get("is_link"),
            filetype=file_information.get("filetype"),
            filesize=file_information.get("filesize"),
            tag=document_type,
        )
        return employee_file

    @classmethod
    def create_files(cls, files):
        """
        Create a list of Employee instances from a list of file information.

        Args:
            files (list): A list of tuples containing document type and file information.

        Returns:
            list: A list of created EmployeeFile instances.
        """
        created_files = []
        for doc_type, files_info in files:
            for file_info in files_info:
                if file_info:
                    created_files.append(cls.create_file(doc_type, file_info))

        return created_files

    @classmethod
    def to_entity(cls, data: Dict, files: Dict) -> Employee:
        """
        Convert a dictionary following a form structure
        into an Employee entity.

        Args:
            data (dict): The data dictionary.
            files (list): A list of file information.

        Returns:
            Employee: The created Horse entity.
        """
        phone = data.get("phone", {})
        employment_information = data.get("employment_information", {})
        address = data.get("address", {})
        emergency_contact = data.get("emergency_contact", {})

        employee = Employee(
            id=data.get("id"),
            name=data.get("name"),
            lastname=data.get("lastname"),
            country_code=phone.get("country_code"),
            area_code=phone.get("area_code"),
            phone=phone.get("number"),
            dni=data.get("dni"),
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
        )

        if files:
            employee_files = cls.create_files(files)
            for file in employee_files:
                if file:
                    employee.files.append(file)

        return employee

    @classmethod
    def from_entity(cls, employee: Employee, documents: bool = True) -> "Dict":
        """
        Convert an Employee entity to a dictionary.

        Args:
            employee (Employee): The Employee entity.
            documents (bool): Whether to include documents.

        Returns:
            dict: The serialized horse data.
        """
        number_of_files = 5
        serialized_employee = {
            "id": employee.id,
            "name": employee.name,
            "lastname": employee.lastname,
            "dni": employee.dni,
            "phone": {
                "country_code": employee.country_code,
                "area_code": employee.area_code,
                "number": employee.phone,
            },
            "employment_information": {
                "profession": employee.profession.value,
                "position": employee.position.value,
                "job_condition": employee.job_condition.value,
                "start_date": employee.start_date,
                "end_date": employee.end_date,
                "is_active": employee.is_active,
            },
            "address": {
                "street": employee.street,
                "number": employee.number,
                "department": employee.department,
                "locality": employee.locality,
                "province": employee.province,
            },
            "emergency_contact": {
                "emergency_contact_name": employee.emergency_contact_name,
                "emergency_contact_phone": employee.emergency_contact_phone,
            },
            "health_insurance": employee.health_insurance,
            "affiliate_number": employee.affiliate_number,
            "email": employee.email,
            "user_id": employee.user_id,
            "inserted_at": employee.inserted_at,
            "updated_at": employee.updated_at,
            "is_deleted": employee.is_deleted,
        }
        if documents:
            serialized_employee["files"] = [
                file.to_dict() for file in employee.files[:number_of_files] if file
            ]
            serialized_employee["files_number"] = len(employee.files)

        return serialized_employee

    @classmethod
    def flat_form(cls, data: Dict) -> "Dict":
        """
        Convert an structured form dictionary to a flat
        representation.
        Args:
            data (dict): The form data dictionary.

        Returns:
            dict: The employee data dictionary.
        """
        phone = data.get("phone", {})
        employment_information = data.get("employment_information", {})
        address = data.get("address", {})
        emergency_contact = data.get("emergency_contact", {})
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "lastname": data.get("lastname"),
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
