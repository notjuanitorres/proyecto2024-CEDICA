from typing import Dict, List
from .models import Horse, HorseMinioFile


class HorseMapper:
    @classmethod
    def create_file(cls, document_type, file_information):
        horse_file = HorseMinioFile(
            filename=file_information.get("filename"),
            filetype=file_information.get("filetype"),
            filesize=file_information.get("filesize"),
            original_filename=file_information.get("original_filename"),
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
    def to_entity(cls, data: Dict, files: List) -> Horse:
        horse = Horse(
            name=data.get("name"),
            birth_date=data.get("birth_date"),
            sex=data.get("sex"),
            breed=data.get("breed"),
            coat=data.get("coat"),
            is_donation=data.get("is_donation"),
            admission_date=data.get("admission_date"),
            assigned_facility=data.get("assigned_facility"),
            ja_type=data.get("ja_type"),
        )

        if files:
            horse_files = cls.create_files(files)
            for file in horse_files:
                if file:
                    horse.minio_files.append(file)

        return horse

    @classmethod
    def from_entity(cls, horse: Horse) -> Dict:
        serialized_horse = {"id": horse.id, "name": horse.name, "birth_date": horse.birth_date, "sex": horse.sex,
                            "breed": horse.breed, "coat": horse.coat, "is_donation": horse.is_donation,
                            "admission_date": horse.admission_date, "assigned_facility": horse.assigned_facility,
                            "ja_type": horse.ja_type.value, "inserted_at": horse.inserted_at,
                            "updated_at": horse.updated_at,
                            "minio_files": [file.to_dict() for file in horse.minio_files if file]}

        return serialized_horse

    @classmethod
    def from_simple_form(cls, data: Dict):
        return {
            "name": data.get("name"),
            "birth_date": data.get("birth_date"),
            "sex": data.get("sex"),
            "breed": data.get("breed"),
            "coat": data.get("coat"),
            "is_donation": data.get("is_donation"),
            "admission_date": data.get("admission_date"),
            "assigned_facility": data.get("assigned_facility"),
            "ja_type": data.get("ja_type"),
        }
