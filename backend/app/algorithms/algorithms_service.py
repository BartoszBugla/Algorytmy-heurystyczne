import itertools
import random
from typing import Callable, List, Dict, Tuple

from fastapi import UploadFile
from app.core.models import IOptimizationAlgorithm
from app.storage import StorageService
import numpy as np
import pandas as pd
import optuna

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

    def trigger_test_by_name(
        self, name: str, fun: str, domain: List[List[float]], params: List[List[float]]
    ):
        algorithm = self._get_instance_by_name(name)

        ranges = [np.arange(start, stop, step) for start, stop, step in params]
        all_combinations = list(itertools.product(*ranges))

        fun_module = functions_service.storage.load_file(fun)
        function = fun_module.__main__

        param_names = [x.name for x in algorithm.params_info]
        other_data = ["number_of_evaluation_fitness_function", "x_best", "f_best"]

        all_keys = param_names + other_data
        results = {key: [] for key in all_keys}

        for combination in all_combinations:
            algorithm = self._get_instance_by_name(name)
            params = combination
            algorithm.solve(function, domain, params)

            for i, p in enumerate(params):
                results[param_names[i]].append(p)

            results["number_of_evaluation_fitness_function"].append(algorithm.number_of_evaluation_fitness_function)
            results["x_best"].append(algorithm.x_best)
            results["f_best"].append(algorithm.f_best)

        results_df = pd.DataFrame(results)
        results_df.to_csv(f"{algorithm.name}_test_results.csv")

    def trigger_optuna_test_by_name(
        self, name: str, fun: str, domain: List[List[float]], params: List[Tuple[float, float, str]], trials_count: int
    ):
        def objective(trial, function, param_dict):
            algorithm = self._get_instance_by_name(name)
            # fun_module = functions_service.storage.load_file(fun)
            # function = fun_module.__main__
            #
            # param_names = [x.name for x in algorithm.params_info]
            #
            # param_ranges = [x for x in params]
            # param_dict = dict(zip(param_names, param_ranges))

            param_choices = []
            for key, value in param_dict.items():
                start, end, var_type = value
                if var_type == "int":
                    param_choices.append(trial.suggest_int(key, start, end))
                elif var_type == "float":
                    param_choices.append(trial.suggest_float(key, start, end))

            algorithm.solve(function, domain, param_choices)

            print(f"{algorithm.f_best}")
            return algorithm.f_best

        algorithm = self._get_instance_by_name(name)
        fun_module = functions_service.storage.load_file(fun)
        function = fun_module.__main__
        param_names = [x.name for x in algorithm.params_info]
        param_ranges = [x for x in params]
        param_dict = dict(zip(param_names, param_ranges))

        study = optuna.create_study(direction="minimize")
        study.optimize(lambda trial: objective(trial, function, param_dict), n_trials=trials_count)
        random_num = random.randint(0, 100000)
        print(f"{name} {random_num} finished with best value {study.best_value} and best params {study.best_params}")
        study.trials_dataframe().to_csv(f"{name}_{random_num}_test_results.csv")

algorithms_service = AlgorithmsService()
