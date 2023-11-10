from fastapi import UploadFile

from app.storage import StorageService


class FunctionsService:
    def __init__(self):
        self.storage = StorageService("functions")

    def trigger_by_name(self, name: str, input: list[float]):
        # @TODO
        return None

    def read_all(self):
        return self.storage.get_files_in_folder()

    def create(self, name: str, upload_file: UploadFile):
        return self.storage.save_file(name, upload_file)

    def delete_by_name(self, name: str):
        return self.storage.delete_file(name)


functions_service = FunctionsService()
