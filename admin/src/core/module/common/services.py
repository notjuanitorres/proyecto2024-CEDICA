import os
from typing import List, Dict
from datetime import datetime, timedelta
from abc import abstractmethod
from urllib3 import HTTPResponse
from ulid import ULID
from minio import Minio
from werkzeug.datastructures import FileStorage
from flask import current_app

# from typing import BinaryIO
FileType = Dict[str, str | int]
FilesType = List[FileType]


class   AbstractStorageServices(object):
    @abstractmethod
    def upload_file(self, file: FileStorage, path: str = ""):
        raise NotImplementedError

    @abstractmethod
    def upload_batch(self, files: List[FileStorage], path: str = ""):
        raise NotImplementedError

    @abstractmethod
    def get_file(self, path: str, filename: str):
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, filename: str):
        raise NotImplementedError

    @abstractmethod
    def presigned_download_url(self, filename: str, path: str = "") -> str:
        raise NotImplementedError

    @abstractmethod
    def presigned_upload_url(self, filename: str, path: str = "") -> str:
        raise NotImplementedError


class StorageServices(AbstractStorageServices):
    def __init__(self):
        # TODO: Remove the hardcoded bucket_name
        self.bucket_name = "grupo19"
        self.expiration_get = 2
        self.storage: Minio = current_app.storage.client

    def upload_file(self, file: FileStorage, path: str = ""):
        ulid: str = ULID().from_datetime(datetime.now()).hex
        filename = self.__construct_path(path, f"{ulid}{file.filename}")
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > 0:
            self.storage.put_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                data=file.stream,
                length=size,
                content_type=file.content_type,
            )
            uploaded_file = {
                "filename": filename,
                "filetype": file.mimetype,
                "filesize": size,
            }
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

    def presigned_download_url(self, filename: str, path: str = "") -> str:
        return self.storage.presigned_get_object(
            self.bucket_name,
            self.__construct_path(path=path, filename=filename),
            expires=timedelta(hours=self.expiration_get),
        )

    def presigned_upload_url(self, filename: str, path: str = "") -> str:
        return self.storage.presigned_put_object(
            self.bucket_name, self.__construct_path(path, filename)
        )

    def delete_file(self, filename: str, path: str = ""):
        self.storage.remove_object(
            self.bucket_name, self.__construct_path(path, filename)
        )

    def __construct_path(self, path: str = "", filename: str = "") -> str:
        return f"{path}{filename}" if path.endswith("/") else f"{path}/{filename}"
