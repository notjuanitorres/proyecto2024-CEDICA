import os
from typing import List, Dict
from datetime import datetime, timedelta
from abc import abstractmethod

from urllib3.exceptions import MaxRetryError
from urllib3 import HTTPResponse
from ulid import ULID
from minio import Minio
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from flask import current_app

# from typing import BinaryIO
FileType = Dict[str, str | int]
FilesType = List[FileType]


class AbstractStorageServices(object):
    @abstractmethod
    def upload_file(self, file: FileStorage, path: str = "", title: str = "") -> Dict | None:
        raise NotImplementedError

    @abstractmethod
    def upload_batch(self, files: List[FileStorage], path: str = ""):
        raise NotImplementedError

    @abstractmethod
    def get_file(self, path: str, filename: str):
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, filename: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def presigned_download_url(self, filename: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def presigned_upload_url(self, filename: str, path: str = "") -> str | None:
        raise NotImplementedError

    @abstractmethod
    def modify_file(self, file: FileStorage, full_path: str) -> bool:
        raise NotImplementedError


class StorageServices(AbstractStorageServices):
    def __init__(self):
        # TODO: Remove the hardcoded bucket_name
        self.bucket_name = "grupo19"
        self.expiration_get = 1
        self.storage: Minio = current_app.storage.client

    def modify_file(self, file: FileStorage, full_path: str) -> bool:
        """Modifies an already existent file in the storage

        :params: file: FileStorage contents of the file
        :params: full_path: str path to the file in the storage
        :return: bool True if the file was modified successfully, False otherwise
        """
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > 0:
            try:
                self.storage.put_object(
                    bucket_name=self.bucket_name,
                    object_name=full_path,
                    data=file.stream,
                    length=size,
                    content_type=file.content_type,
                )
            except MaxRetryError as e:
                print("No se pudo establecer conexion con minio. Error: ", e)
                return False

        return True

    def upload_file(self, file: FileStorage, path: str = "", title: str = ""):
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
        uploaded_files = {}
        if isinstance(files, list):
            uploaded_files = [
                self.upload_file(file, path) for file in files if file and file.filename.strip()
            ]
        return uploaded_files

    def get_file(self, path: str, filename: str):
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

    def presigned_download_url(self, filename: str) -> str:
        try:
            return self.storage.presigned_get_object(
                self.bucket_name,
                filename,
                expires=timedelta(hours=self.expiration_get),
            )
        except MaxRetryError as e:
            print("No se pudo establecer conexion con minio. Error: ", e)
            return None

    def presigned_upload_url(self, filename: str, path: str = "") -> str:
        try:
            return self.storage.presigned_put_object(
                self.bucket_name, self.__construct_path(path, filename)
            )
        except MaxRetryError as e:
            print("No se pudo establecer conexion con minio. Error: ", e)
            return None

    def delete_file(self, filename: str) -> None:
        try:
            self.storage.remove_object(
                self.bucket_name, filename
            )
            return True
        except MaxRetryError as e:
            print("No se pudo establecer conexion con minio. Error: ", e)
            return False

    def __construct_path(self, path: str = "", filename: str = "") -> str:
        return f"{path}{filename}" if path.endswith("/") else f"{path}/{filename}"
