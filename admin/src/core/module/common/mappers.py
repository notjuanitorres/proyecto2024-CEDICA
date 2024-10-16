from typing import Dict
from .models import File


class FileMapper:
    @classmethod
    def to_form(cls, file: dict):
        file_dict = {
            "title": file["title"],
            "url": file["path"] if file["is_link"] else None,
            "upload_type": "url" if file["is_link"] else "file",
            "tag": file["tag"],
        }

        return file_dict
