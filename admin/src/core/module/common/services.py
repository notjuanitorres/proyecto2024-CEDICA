import os
from typing import List, Dict
from datetime import datetime, timedelta
from abc import abstractmethod

from urllib3.exceptions import MaxRetryError
from urllib3 import HTTPResponse
from ulid import ULID
from minio import Minio
from werkzeug.datastructures import FileStorage

from flask import current_app

FileType = Dict[str, str | int]
FilesType = List[FileType]


class AbstractStorageServices(object):
    """
    Abstract class defining storage service methods that must be implemented.

    Methods:
        upload_file: Uploads a single file.
        upload_batch: Uploads multiple files.
        get_file: Retrieves a file from storage.
        delete_file: Deletes a file from storage.
        presigned_download_url: Generates a presigned URL for downloading.
        presigned_upload_url: Generates a presigned URL for uploading.
        modify_file: Modifies an existing file in storage.
        get_profile_image: Retrieves a profile image from storage.
    """

    @abstractmethod
    def upload_file(self, file: FileStorage, path: str = "", title: str = "") -> Dict | None:
        """Uploads a single file to the storage system.

        Args:
            file (FileStorage): The file to upload.
            path (str, optional): The path to store the file in. Defaults to "".
            title (str, optional): The title or name of the file. Defaults to "".

        Returns:
            Dict | None: Metadata of the uploaded file, or None if upload fails.
        """
        raise NotImplementedError

    @abstractmethod
    def upload_batch(self, files: List[FileStorage], path: str = ""):
        """Uploads multiple files to the storage system.

        Args:
            files (List[FileStorage]): List of files to upload.
            path (str, optional): The path to store the files in. Defaults to "".
        """
        raise NotImplementedError

    @abstractmethod
    def get_file(self, path: str, filename: str):
        """Retrieves a file from storage.

        Args:
            path (str): The directory path to the file.
            filename (str): The name of the file.

        Returns:
            The file data.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, filename: str) -> bool:
        """Deletes a file from storage.

        Args:
            filename (str): The name of the file to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_batch(self, filenames: List[str]) -> bool:
        """Deletes a batch of files from storage.

        Args:
            filenames (List[str]): The names of the files to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def presigned_download_url(self, filename: str) -> str | None:
        """Generates a presigned URL for downloading a file.

        Args:
            filename (str): The name of the file to download.

        Returns:
            str | None: A presigned download URL, or None if generation fails.
        """
        raise NotImplementedError

    @abstractmethod
    def presigned_upload_url(self, filename: str, path: str = "") -> str | None:
        """Generates a presigned URL for uploading a file.

        Args:
            filename (str): The name of the file to upload.
            path (str, optional): The path for the file. Defaults to "".

        Returns:
            str | None: A presigned upload URL, or None if generation fails.
        """
        raise NotImplementedError

    @abstractmethod
    def modify_file(self, file: FileStorage, full_path: str) -> bool:
        """Modifies an existing file in storage.

        Args:
            file (FileStorage): The file to modify.
            full_path (str): The full path to the file.

        Returns:
            bool: True if successful, False otherwise.
        """
        raise NotImplementedError
    @abstractmethod
    def get_profile_image(self, filename: str) -> bytes:
        """Retrieves a profile image from storage.

        Args:
            filename (str): The name of the file.

        Returns:
            bytes: The profile image data.
        """
        raise NotImplementedError

    @abstractmethod
    def get_profile_image_url(self, filename: str) -> str:
        """Retrieves a profile image from storage.

        Args:
            filename (str): The name of the file.

        Returns:
            The file data.
        """
        raise NotImplementedError


class StorageServices(AbstractStorageServices):
    """
    Implementation of storage services using a MinIO backend.

    Attributes:
        bucket_name (str): The name of the storage bucket.
        expiration_get (int): Time (in hours) before presigned URLs expire.
        storage (Minio): The Minio client instance.

    Methods:
        upload_file: Uploads a file to the storage bucket.
        upload_batch: Uploads a batch of files to the storage bucket.
        get_file: Retrieves a file from storage.
        presigned_download_url: Generates a presigned URL for downloading a file.
        presigned_upload_url: Generates a presigned URL for uploading a file.
        delete_file: Deletes a file from storage.
        modify_file: Modifies an existing file in storage.
    """

    def __init__(self):
        """Initializes the StorageServices class with default bucket settings."""
        # TODO: Remove the hardcoded bucket_name
        self.bucket_name = "grupo19"
        self.expiration_get = 1
        self.storage: Minio = current_app.storage.client

    def upload_file(self, file: FileStorage, path: str = "", title: str = ""):
        """Uploads a single file to the storage bucket.

        Args:
            file (FileStorage): The file to upload.
            path (str, optional): The directory path for storing the file. Defaults to "".
            title (str, optional): The title or name of the file. Defaults to "".

        Returns:
            dict: Metadata of the uploaded file or None if an error occurs.
        """
        ulid: str = ULID().from_datetime(datetime.now()).hex
        filename = self.__construct_path(path, f"{ulid}{title}")
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        uploaded_file = {}
        if size > 0:
            try:
                self.storage.put_object(
                    bucket_name=self.bucket_name,
                    object_name=filename,
                    data=file.stream,
                    length=size,
                    content_type=file.content_type,
                )
                uploaded_file = {
                    "path": filename,
                    "filetype": file.mimetype,
                    "filesize": size,
                    "title": title,
                    "is_link": False,
                }
            except MaxRetryError as e:
                uploaded_file = None
                print("No se pudo establecer conexion con minio. Error: ", e)

        return uploaded_file

    def upload_batch(self, files: List[FileStorage], path: str = "") -> FilesType:
        """Uploads a batch of files to the storage bucket.

        Args:
            files (List[FileStorage]): List of files to upload.
            path (str, optional): The directory path for storing the files. Defaults to "".

        Returns:
            list: Metadata of the uploaded files.
        """
        uploaded_files = {}
        if isinstance(files, list):
            uploaded_files = [
                self.upload_file(file, path) for file in files if file and file.filename.strip()
            ]
        return uploaded_files

    def get_file(self, path: str, filename: str):
        """Retrieves a file from storage.

        Args:
            path (str): The directory path to the file.
            filename (str): The name of the file.

        Returns:
            The file data.
        """
        response: HTTPResponse
        try:
            response = self.storage.get_object(
                self.bucket_name,
                self.__construct_path(path=path, filename=filename),
            )
        finally:
            response.close()
            response.release_conn()
        return response.data


    def get_profile_image(self, filename: str):
        response: HTTPResponse
        if filename == None:
            filename='users/default_profile_image.png'
        response = self.storage.get_object(
            self.bucket_name,
            filename,
        )
        return response.data
    
    def presigned_download_url(self, filename: str) -> str:
        """Generates a presigned URL for downloading a file.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The presigned download URL.
        """
        try:
            return self.storage.presigned_get_object(
                self.bucket_name,
                filename,
                expires=timedelta(hours=self.expiration_get),
            )
        except MaxRetryError as e:
            print("No se pudo establecer conexion con minio. Error: ", e)
            return ""

    def presigned_upload_url(self, filename: str, path: str = "") -> str:
        """Generates a presigned URL for uploading a file.

        Args:
            filename (str): The name of the file.
            path (str, optional): The directory path for storing the file. Defaults to "".

        Returns:
            str: The presigned upload URL.
        """
        try:
            return self.storage.presigned_put_object(
                self.bucket_name, self.__construct_path(path, filename)
            )
        except MaxRetryError as e:
            print("No se pudo establecer conexion con minio. Error: ", e)
            return ""

    def delete_file(self, filename: str) -> bool:
        """Deletes a file from storage.

        Args:
            filename (str): The name of the file.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        try:
            self.storage.remove_object(
                self.bucket_name, filename
            )
            return True
        except MaxRetryError as e:
            print("No se pudo establecer conexion con minio. Error: ", e)
            return False

    def delete_batch(self, filenames: List[str]) -> bool:
        """Deletes a batch of files from storage.

        Args:
            filenames (List[str]): The names of the files to delete.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        try:
            for filename in filenames:
                self.storage.remove_object(
                    self.bucket_name, filename
                )
            return True
        except MaxRetryError as e:
            print("No se pudo establecer conexion con minio. Error: ", e)
            return False

    def __construct_path(self, path: str = "", filename: str = "") -> str:
        """Constructs a file path by concatenating the path and filename.

        Args:
            path (str, optional): The directory path. Defaults to "".
            filename (str, optional): The file name. Defaults to "".

        Returns:
            str: The constructed file path.
        """
        return f"{path}{filename}" if path.endswith("/") else f"{path}/{filename}"

