import math
import os
from typing import List, Callable, Dict, Optional

import numpy as np

from PVS_alg.pvs_classes import PVSReader, PVSWriter
from PVS_alg.interfaces import IOptimizationAlgorithm, ParamInfo, IStateWriter


class PVS(IOptimizationAlgorithm):
    def __init__(self):
        super().__init__("PVS")

        self.params_info: List[ParamInfo] = [
            ParamInfo("ps", "Population size", math.inf, 3),
            ParamInfo("gen", "Number of generations", math.inf, 1),
        ]

        self.Y: Optional[ValueCache] = None

        self.writer: PVSWriter = PVSWriter(self)
        self.reader: PVSReader = PVSReader()

    def solve(self, fun: Callable, domain, parameters: List[float]) -> None:
        if os.path.exists("pvs_state.txt"):
            start_gen, start_eval_count, population = self.reader.load_from_file_state_of_algorithm("pvs_state.txt")
            self.gen_num = start_gen
            self.number_of_evaluation_fitness_function = start_eval_count
            self.X = population

        ps, gen = parameters

        dv = len(domain)
        np_domain = np.array(domain)

        if not self.X:
            self.X = np.random.uniform(np_domain[:, 0], np_domain[:, 1], (ps, dv))

        self.Y = ValueCache(fun, self)

        self.X = np.array(sorted(self.X, key=lambda x: self.Y.get(x), reverse=False))

        r = np.array([0, 0, 0])

        last_best = self.X[: ps // 10]

        for _ in range(self.gen_num, gen):
            for i in range(ps):
                r[0] = i

                while r[1] == r[0]:
                    r[1] = np.random.randint(0, ps)

                while r[1] == r[2] or r[0] == r[2]:
                    r[2] = np.random.randint(0, ps)

                D = (1 / ps) * r
                R = np.random.rand(3)
                V = R * (1 - D)

                d1, d2, d3 = D
                v1, v2, v3 = V

                x = np.absolute(d3 - d1)
                y = np.absolute(d3 - d2)
                x1 = (v3 * x) / (v1 - v3)
                y1 = (v2 * x) / (v1 - v3)

                v_co = v1 / (v1 - v3)

                if v3 < v1:
                    if (y - y1) > x1:
                        prob_new_sol = self.X[r[0]] + np.random.random() * v_co * (self.X[r[0]] - self.X[r[2]])

                    else:
                        prob_new_sol = self.X[r[0]] + np.random.random() * (self.X[r[0]] - self.X[r[1]])

                else:
                    prob_new_sol = self.X[r[0]] + np.random.random() * (self.X[r[2]] - self.X[r[0]])

                if self.Y.get(prob_new_sol) < self.Y.get(self.X[r[0]]):
                    self.X[r[0]] = prob_new_sol

            self.X = np.array(sorted(self.X, key=lambda x: self.Y.get(x), reverse=False))

            for i, solution in enumerate(last_best):
                if solution not in self.X:
                    self.X[-1 - i] = solution

            self.X = np.array(sorted(self.X, key=lambda x: self.Y.get(x), reverse=False))
            last_best = self.X[: ps // 10]
            self.gen_num += 1

            if self.gen_num % 10 == 0:
                self.writer.save_to_file_state_of_algorithm(f"pvs_state.txt")

        self.x_best = self.X[0]
        self.f_best = self.Y.get(self.X[0])


class ValueCache:
    def __init__(self, fun, algorithm: PVS):
        self.fun: callable = fun
        self.values: Dict = {}
        self.pvs = algorithm

    def fun_with_calc(self, x):
        self.pvs.number_of_evaluation_fitness_function += 1
        return self.fun(x)

    def get(self, x):
        if f"{tuple(x)}" not in self.values:
            self.values[f"{tuple(x)}"] = self.fun_with_calc(x)
            return self.values[f"{tuple(x)}"]

        return self.values[f"{tuple(x)}"]


pvs = PVS()
