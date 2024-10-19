from typing import Dict


class FileMapper:
    @classmethod
    def to_form(cls, file: Dict) -> Dict:
        """
        Converts a file dictionary to a form-friendly dictionary.

        Args:
            file (dict): A dictionary containing file details, including
                         "title", "path", "is_link", and "tag".

        Returns:
            dict: A dictionary with form-compatible fields such as
                  "title", "url", "upload_type", and "tag".
        """
        file_dict = {
            "title": file["title"],
            "url": file["path"] if file["is_link"] else None,
            "upload_type": "url" if file["is_link"] else "file",
            "tag": file["tag"],
        }

        return file_dict

    @classmethod
    def file_from_form(cls, data: Dict) -> dict:
        """
        Transforms edit form data into a dictionary for updating a file.

        This method creates a dictionary that can be used to update an
        existing file's details, based on the form data. In cases where
        the file is linked via URL, the "path" field is set. This method
        should only be called if there is no new file to upload for
        MinIO file updates.

        Args:
            data (Dict): A dictionary containing form data with keys such as
                         "title", "upload_type", "tag", and optionally "url"
                         if the file is a URL.

        Returns:
            dict: A dictionary with updated file information including "title",
                  "is_link", "tag", and optionally "path" for URL-based files.
        """
        temp = {
            "title": data.get("title"),
            "is_link": data.get("upload_type") == "url",
            "tag": data.get("tag"),
        }

        if data.get("upload_type") == "url":
            temp["path"] = data.get("url")

        return temp
