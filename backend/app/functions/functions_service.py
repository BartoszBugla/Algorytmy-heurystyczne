from typing import Any

from fastapi import UploadFile

from app.storage import StorageService

ACCEPTED_EXTENSION = "py"


class FunctionsService:
    def __init__(self):
        self.storage = StorageService("functions", ACCEPTED_EXTENSION)

    def trigger_by_name(self, name: str, input: list[float]):
        function: Any = self.storage.load_file(name)

        # add proper error handling here
        if function is None:
            return None

        # https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
        return function.__main__(input)

    def read_all(self):
        funcs = self.storage.get_files_in_folder()
        no_extension = map(lambda x: x.split(".")[0], funcs)
        return no_extension

    def create(self, name: str, upload_file: UploadFile):
        return self.storage.save_file(name, upload_file)

    def delete_by_name(self, name: str):
        return self.storage.delete_file(f"{name}.{ACCEPTED_EXTENSION}")


functions_service = FunctionsService()
