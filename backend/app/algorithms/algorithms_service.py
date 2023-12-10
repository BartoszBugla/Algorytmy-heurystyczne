from typing import Callable, List

from fastapi import UploadFile

from app.storage import StorageService
import numpy as np


class AlgorithmsService:
    def __init__(self):
        self.storage = StorageService("algorithms")
        self.fun_storage = StorageService("functions")

    def trigger_by_name(self, name: str, fun: str, domain: List[List[float]], params: List[int]):
        algo_module = self.storage.load_file(name)
        fun_module = self.fun_storage.load_file(fun)

        algorithm = algo_module.PVS()
        function = fun_module.__main__

        return algorithm.solve(function, domain, params)

    def read_all(self):
        return self.storage.get_files_in_folder()

    def create(self, name: str, upload_file: UploadFile):
        return self.storage.save_file(name, upload_file)

    def delete_by_name(self, name: str):
        return self.storage.delete_file(name)


algorithms_service = AlgorithmsService()
