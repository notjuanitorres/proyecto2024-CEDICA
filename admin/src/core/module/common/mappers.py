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

    @classmethod
    def file_from_form(cls, data: Dict):
        """
        Transforms edit form data into a dictionary that can be used to update a file.

        :param data: Dictionary with the form data.
        In the case of minio files this should only be called if there is not a new file to upload.
        """
        temp = {
            "title": data.get("title"),
            "is_link": data.get("upload_type") == "url",
            "tag": data.get("tag"),
        }

        if data.get("upload_type") == "url":
            temp["path"] = data.get("url")

        return temp
