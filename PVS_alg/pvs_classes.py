import numpy as np

from PVS_alg.interfaces import (
    IStateReader,
    IStateWriter,
    IGeneratePDFReport,
    IGenerateTextReport,
    IOptimizationAlgorithm,
)

from typing import Optional, List, Dict


class PVSWriter(IStateWriter):
    def __init__(self, pvs: IOptimizationAlgorithm):
        self._pvs: IOptimizationAlgorithm = pvs

    def save_to_file_state_of_algorithm(self, path: str) -> None:
        def _save_population(f):
            for i in range(len(self._pvs.X)):
                for j in range(len(self._pvs.X[0])):
                    f.write(f"{self._pvs.X[i][j]} ")
                f.write(f"{self._pvs.Y.get(self._pvs.X[i])}")
                f.write("\n")

        with open(path, "w") as file:
            file.write(f"{self._pvs.gen_num}\n")
            file.write(f"{self._pvs.number_of_evaluation_fitness_function}\n")
            _save_population(file)


class PVSReader(IStateReader):
    def load_from_file_state_of_algorithm(self, path: str) -> (int, int, np.ndarray):
        with open(path, "r") as file:
            lines = file.readlines()
            start_gen = int(lines[0])
            start_eval_count = int(lines[1])
            population = []
            for row in lines[2:]:
                row = row.split(" ")[:-1]
                row = [float(x) for x in row]
                population.append(row)

            population = np.array(population)
            return start_gen, start_eval_count, population
