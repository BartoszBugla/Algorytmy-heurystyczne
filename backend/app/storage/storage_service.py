import os
import importlib
import dill as pickle

from fastapi import UploadFile

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
        return os.path.join(self.storage_path, f"{fileName}.{self.file_extension}")

    def load_file(self, fileName: str):
        module_name = f"storage.{self.storage_name}.{fileName}"

        try:
            return importlib.import_module(module_name)
        except ImportError:
            return None

    def get_files_in_folder(self):
        """List all files in folder."""
        return os.listdir(os.path.join(self.storage_path))

    def delete_file(self, fileName: str):
        """Delete file by name."""
        if os.path.exists(self.__get_file_path(fileName)):
            return os.remove(self.__get_file_path(fileName))
        else:
            return None

    def save_file(self, fileName: str, upload_file: UploadFile):
        with open(self.__get_file_path(fileName), "wb") as file:
            file.write(upload_file.file.read())


base_storage_service = StorageService()
