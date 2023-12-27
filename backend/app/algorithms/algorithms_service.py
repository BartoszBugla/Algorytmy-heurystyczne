from typing import Callable, List

from fastapi import UploadFile
from app.core.models import IOptimizationAlgorithm
from app.storage import StorageService
import numpy as np

from app.algorithms.algorithms_models import AlgorithmMetadata, ParamInfo
from app.functions.functions_service import functions_service


class AlgorithmsService:
    def __init__(self):
        self.storage = StorageService("algorithms")

    def _get_instance_by_name(self, name: str) -> IOptimizationAlgorithm:
        algo_module = self.storage.load_file(name)

        algo: IOptimizationAlgorithm = getattr(algo_module, name)()

        return algo

    def read_algorithm_metadata(self, name: str) -> AlgorithmMetadata:
        algorithm = self._get_instance_by_name(name)

        return AlgorithmMetadata(
            name=algorithm.name,
            params_info=[
                ParamInfo(
                    name=x.name,
                    description=x.description,
                    upper_bound=x.upper_bound,
                    lower_bound=x.lower_bound,
                )
                for x in algorithm.params_info
            ],
        )

    def trigger_by_name(
        self, name: str, fun: str, domain: List[List[float]], params: List[float]
    ):
        algorithm = self._get_instance_by_name(name)

        fun_module = functions_service.storage.load_file(fun)
        function = fun_module.__main__

        return algorithm.solve(function, domain, params)

    def read_all(self):
        algorithms = self.storage.get_files_in_folder()
        no_extension = list(map(lambda x: x.split(".")[0], algorithms))
        return no_extension

    def create(self, name: str, upload_file: UploadFile):
        return self.storage.save_file(name, upload_file)

    def delete_by_name(self, name: str):
        return self.storage.delete_file(name)


algorithms_service = AlgorithmsService()
