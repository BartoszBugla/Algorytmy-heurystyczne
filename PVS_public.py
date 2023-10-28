import numpy as np

from random import random
import pandas as pd
from funcs import *


class ValueCache:
    values = {}
    number_of_fun_calculations = 0

    def fun_with_calc(self, x):
        self.number_of_fun_calculations += 1
        return self.fun(x)

    def __init__(self, fun):
        self.fun = fun

    def get(self, x):
        if f"{tuple(x)}" not in self.values:
            self.values[f"{tuple(x)}"] = self.fun_with_calc(x)
            return self.values[f"{tuple(x)}"]

        return self.values[f"{tuple(x)}"]


class PVS:
    """
    Dopasowane do interfesju z zadania
    """

    def __init__(self):
        self.name = "PVS"
        self.x_best = None
        self.f_best = None
        self.number_of_evaluationF_fitness_function = None

    # step 1
    def solve(self, fun, PS, GEN, DV, LB_X, UB_X, LB_Y=None, UB_Y=None):
        X = []

        if LB_Y and UB_Y and DV == 2:
            # for bukin case
            x = np.random.uniform(LB_X, UB_X, (PS, 1))
            y = np.random.uniform(LB_Y, UB_Y, (PS, 1))
            X = np.concatenate((x, y), axis=1)
        else:
            X = np.random.uniform(LB_X, UB_X, (PS, DV))

        Y = ValueCache(fun)

        X = np.array(sorted(X, key=lambda x: Y.get(x), reverse=False))

        r = np.array([0, 0, 0])

        last_best = X[: PS // 10]

        for _ in range(GEN):
            for i in range(PS):
                r[0] = i

                while r[1] == r[0]:
                    r[1] = np.random.randint(0, PS)

                while r[1] == r[2] or r[0] == r[2]:
                    r[2] = np.random.randint(0, PS)

                D = (1 / PS) * r
                R = np.random.rand(3)
                V = R * (1 - D)

                D1, D2, D3 = D
                V1, V2, V3 = V

                x = np.absolute(D3 - D1)
                y = np.absolute(D3 - D2)
                x1 = (V3 * x) / (V1 - V3)
                y1 = (V2 * x) / (V1 - V3)

                V_co = V1 / (V1 - V3)

                prob_new_sol = 0
                if V3 < V1:
                    if (y - y1) > x1:
                        prob_new_sol = X[r[0]] + np.random.random() * V_co * (
                            X[r[0]] - X[r[2]]
                        )

                    else:
                        prob_new_sol = X[r[0]] + np.random.random() * (
                            X[r[0]] - X[r[1]]
                        )

                else:
                    prob_new_sol = X[r[0]] + np.random.random() * (X[r[2]] - X[r[0]])

                if Y.get(prob_new_sol) < Y.get(X[r[0]]):
                    X[r[0]] = prob_new_sol

                for k in range(PS - 1):
                    if all(X[k] == X[k + 1]):
                        i = np.random.randint(0, DV)
                        X[k + 1][i] = LB_X + np.random.random() * (UB_X - LB_X)

            X = np.array(sorted(X, key=lambda x: Y.get(x), reverse=False))
            for i, solution in enumerate(last_best):
                if solution not in X:
                    X[-1 - i] = solution
            X = np.array(sorted(X, key=lambda x: Y.get(x), reverse=False))
            last_best = X[: PS // 10]

        self.x_best = X[0]
        self.f_best = Y.get(X[0])
        self.number_of_evaluationF_fitness_function = Y.number_of_fun_calculations

        return Y.get(X[0])


pvs = PVS()
