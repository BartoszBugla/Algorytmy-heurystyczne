import os
import shutil
import pickle

from fastapi import UploadFile

from app.core.config import config


class StorageService:
    def __init__(self, storage_name: str = ""):
        self.storage_path = os.path.join(config.STORAGE_DIR, storage_name)

    def __get_file_path(self, fileName: str):
        return os.path.join(self.storage_path, f"{fileName}.pkl")

    def list_all_folders(self):
        """List all folders."""
        return os.listdir(config.STORAGE_DIR)

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
            serialized_file = pickle.dumps(upload_file.file)
            file.write(serialized_file)


base_storage_service = StorageService()
