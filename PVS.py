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
    name = "PVS"
    generation = 0

    def __init__(self):
        pass

    # step 1
    def solve(self, fun, PS, FE, DV, LB, UB):
        X = np.random.uniform(LB, UB, (PS, DV))
        Y = ValueCache(fun)
        X = sorted(X, key=lambda x: Y.get(x), reverse=False)
        if_1 = 0
        if_2 = 0
        if_3 = 0
        r = np.array([0, 0, 0])
        # import matplotlib.pyplot as plt

        for _ in range(FE):
            # print(
            #     [np.append(x, Y.get(x)) for x in X],
            #     pd.DataFrame(
            #         [np.append(x, Y.get(x)) for x in X],
            #         columns=["First Argument", "Second Argument", "Value"],
            #     ),
            # )

            # plt.scatter([Y.get(x) for x in X], np.zeros(PS))
            # plt.show()

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
                        if_1 += 1

                    else:
                        prob_new_sol = X[r[0]] + np.random.random() * (
                            X[r[0]] - X[r[1]]
                        )
                        if_2 += 1

                else:
                    prob_new_sol = X[r[0]] + np.random.random() * (X[r[2]] - X[r[0]])
                    if_3 += 1

                if Y.get(prob_new_sol) < Y.get(X[r[0]]):
                    X[r[0]] = prob_new_sol

                for k in range(PS - 1):
                    if all(X[k] == X[k + 1]):
                        i = np.random.randint(0, DV)
                        X[k + 1][i] = LB + np.random.random() * (UB - LB)

            X = sorted(X, key=lambda x: Y.get(x), reverse=False)
        print(if_1, if_2, if_3)
        return (X[0], Y.get(X[0]))
