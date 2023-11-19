import math
from typing import List, Callable

import numpy as np

from PVS_alg.pvs_classes import ValueCache, PVSReader
from PVS_alg.interfaces import IOptimizationAlgorithm, ParamInfo, IStateWriter


class PVS(IOptimizationAlgorithm):
    """
    Dopasowane do interfesju z zadania
    """

    def __init__(self):
        super().__init__("PVS")

        self.params_info: List[ParamInfo] = [
            ParamInfo("ps", "Population size", math.inf, 3),
            ParamInfo("gen", "Number of generations", math.inf, 1),
            ParamInfo("dv", "number of dimensions to look for solution in", math.inf, 1),
            ParamInfo("lb_x", "lower bound of x", math.inf, -math.inf),
            ParamInfo("ub_x", "upper bound of x", math.inf, -math.inf),
            ParamInfo("lb_y", "lower bound of y", math.inf, -math.inf),
            ParamInfo("ub_y", "upper bound of y", math.inf, -math.inf),
        ]

    def solve(self, fun: Callable, domain, parameters: List[float]) -> None:
        ps, gen, dv, lb_x, ub_x, lb_y, ub_y = parameters

        if lb_y and ub_y and dv == 2:
            # for bukin case
            x = np.random.uniform(lb_x, ub_x, (ps, 1))
            y = np.random.uniform(lb_y, ub_y, (ps, 1))
            X = np.concatenate((x, y), axis=1)

        else:
            X = np.random.uniform(lb_x, ub_x, (ps, dv))

        Y = ValueCache(fun)

        X = np.array(sorted(X, key=lambda x: Y.get(x), reverse=False))

        r = np.array([0, 0, 0])

        last_best = X[: ps // 10]

        for _ in range(gen):
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
                        prob_new_sol = X[r[0]] + np.random.random() * v_co * (X[r[0]] - X[r[2]])

                    else:
                        prob_new_sol = X[r[0]] + np.random.random() * (X[r[0]] - X[r[1]])

                else:
                    prob_new_sol = X[r[0]] + np.random.random() * (X[r[2]] - X[r[0]])

                if Y.get(prob_new_sol) < Y.get(X[r[0]]):
                    X[r[0]] = prob_new_sol

                for k in range(ps - 1):
                    if all(X[k] == X[k + 1]):
                        i = np.random.randint(0, dv)
                        X[k + 1][i] = lb_x + np.random.random() * (ub_x - lb_x)

            X = np.array(sorted(X, key=lambda x: Y.get(x), reverse=False))

            for i, solution in enumerate(last_best):
                if solution not in X:
                    X[-1 - i] = solution

            X = np.array(sorted(X, key=lambda x: Y.get(x), reverse=False))
            last_best = X[: ps // 10]

        self.x_best = X[0]
        self.f_best = Y.get(X[0])
        self.number_of_evaluation_fitness_function = Y.number_of_fun_calculations

        return (X[0], Y.get(X[0]))


pvs = PVS()
