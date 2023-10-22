import numpy as np

from random import random
import pandas as pd
from funcs import *


class PVS:
    name = "PVS"
    generation = 0

    def __init__(self):
        pass

    # step 1
    def solve(self, fun, PS, FE, DV, LB, UB):
        X = np.random.uniform(LB, UB, (PS, DV))

        r = np.array([0, 0, 0])

        solution = 0

        for _ in range(FE):
            solution = X[0]
            for i in range(PS):
                X = sorted(X, key=lambda x: fun(x), reverse=False)
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

                if fun(prob_new_sol) < fun(solution):
                    solution = prob_new_sol
                    X[r[0]] = prob_new_sol

                for k in range(PS - 1):
                    if all(X[k] == X[k + 1]):
                        i = np.random.randint(0, DV)
                        X[k + 1][i] = LB + np.random.random() * (UB - LB)

        return (solution, fun(solution))
