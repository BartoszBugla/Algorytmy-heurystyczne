import os
import importlib

from typing import Any
from fastapi import UploadFile, HTTPException

from app.core.config import config


class StorageService:
    @staticmethod
    def list_all_folders():
        """List all folders."""
        return os.listdir(config.STORAGE_DIR)

    def __init__(self, storage_name: str = "", file_extension: str = "py"):
        self.file_extension = file_extension
        self.storage_name = storage_name
        self.storage_path = os.path.join(config.STORAGE_DIR, storage_name)

    def __get_file_path(self, fileName: str):
        fileName = fileName.replace(" ", "_")

        return os.path.join(self.storage_path, f"{fileName}")

    def load_file(self, fileName: str) -> Any:
        module_name = f"storage.{self.storage_name}.{fileName}"

        try:
            return importlib.import_module(module_name)
        except ImportError:
            raise HTTPException(
                status_code=404, detail=f"File with given name does not exist."
            )

    def get_files_in_folder(self):
        """List all files in folder."""
        files = os.listdir(os.path.join(self.storage_path))
        filtered = list(filter(lambda x: x != "__pycache__", files))
        return list(filtered)

    def delete_file(self, fileName: str):
        """Delete file by name."""
        if os.path.exists(self.__get_file_path(fileName)):
            return os.remove(self.__get_file_path(fileName))
        else:
            return None

    def save_file(self, fileName: str, upload_file: UploadFile):
        if fileName.split(".")[-1] != self.file_extension:
            raise HTTPException(
                status_code=400, detail=f"File extension must be {self.file_extension}"
            )

        with open(self.__get_file_path(fileName), "wb") as file:
            file.write(upload_file.file.read())
            return file


base_storage_service = StorageService()
