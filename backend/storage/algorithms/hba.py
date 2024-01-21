import math
from typing import List, Callable, Dict, Optional, TypedDict

import numpy as np
import os
import random

from storage.algorithms.interfaces import (
    IStateReader,
    IStateWriter,
    IGeneratePDFReport,
    IGenerateTextReport,
    IOptimizationAlgorithm,
    ParamInfo,
)

class HBAWriter(IStateWriter):
    pass

class HBAReader(IStateReader):
    pass
class HBAGeneratePDFReport(IGeneratePDFReport):
    pass

class hba(IOptimizationAlgorithm):
    def __init__(self):
        super().__init__("HBA")

        self.params_info: List[ParamInfo] = [
            ParamInfo("population_base_size", "Population base size", math.inf, 3),
            ParamInfo("t_max", "Number of generations", math.inf, 1),
            ParamInfo("param_c", "param_c", 3, 0.5),
            ParamInfo("param_b", "param_b", 8, 0.5),
        ]

        # self.writer: HBAWriter = HBAWriter()
        # self.reader: HBAReader = HBAReader()

    def solve(self, test_function: Callable, domain: List[List[float]], parameters: List[float]) -> List[float]:
        domain = np.array(domain)
        lower_bound = domain[0]
        upper_bound = domain[1]
        population_base_size, t_max, param_c, param_b = parameters
        population_base_size = int(population_base_size)
        t_max = int(t_max)
        self.number_of_evaluation_fitness_function = 0
        eps = np.finfo(float).eps
        dimension = len(lower_bound)
        population_real_size = population_base_size * dimension ** 2

        # Initialize candidates
        candidates = np.random.uniform(low=lower_bound, high=upper_bound, size=(population_real_size, dimension))
        
        # Initialize fitness table
        fit_table = np.array([test_function(candidate) for candidate in candidates])
        
        # Initialize prey
        f_prey = np.min(fit_table)
        x_prey = candidates[np.argmin(fit_table)]

        # Start the algorithm
        for t in range(1, t_max + 1):
            a = param_c * np.exp(-t / t_max)

            for i in range(1, population_real_size):
                intensivity = (np.square(candidates[i] - candidates[i - 1]) / (4 * np.pi * (np.square(x_prey - candidates[i]) + eps)))

                if np.random.rand() < 0.5:
                    flag = 1 if np.random.rand() <= 0.5 else -1
                    x_new = x_prey + (flag * param_b * intensivity * x_prey) + \
                            flag * np.random.rand() * a * (x_prey - candidates[i]) * \
                            np.abs(np.cos(2 * np.pi * np.random.rand()) * (1 - np.cos(2 * np.pi * np.random.rand())))
                else:
                    flag = 1 if np.random.rand() <= 0.5 else -1
                    x_new = x_prey + (flag * np.random.rand() * a * x_prey - candidates[i])

                f_new = test_function(x_new)

                if f_new <= fit_table[i]:
                    candidates[i] = x_new
                    fit_table[i] = f_new

                if f_new <= f_prey:
                    x_prey = x_new
                    f_prey = f_new

        self.x_best = x_prey
        self.f_best = f_prey
        return x_prey