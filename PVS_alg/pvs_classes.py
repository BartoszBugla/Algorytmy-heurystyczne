from PVS_alg.interfaces import (
    IStateReader,
    IStateWriter,
    IGeneratePDFReport,
    IGenerateTextReport,
    IOptimizationAlgorithm,
)

from typing import Optional, List, Dict

from pvs import PVS


class PVSWriter(IStateWriter):
    def __init__(self, pvs: PVS):
        self.pvs: PVS = pvs

    def save_to_file_state_of_algorithm(self, path: str) -> None:
        with open(path, "w") as file:
            file.write(self.pvs.)
            file.write(self.pvs.)


class PVSReader(IStateReader):
    def load_from_file_state_of_algorithm(self, path: str) -> None:
        pass


class ValueCache:
    def __init__(self, fun):
        self.fun: callable = fun
        self.values: Dict = {}
        self.number_of_fun_calculations: int = 0

    def fun_with_calc(self, x):
        self.number_of_fun_calculations += 1
        return self.fun(x)

    def get(self, x):
        if f"{tuple(x)}" not in self.values:
            self.values[f"{tuple(x)}"] = self.fun_with_calc(x)
            return self.values[f"{tuple(x)}"]

        return self.values[f"{tuple(x)}"]
