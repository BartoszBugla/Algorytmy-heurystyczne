import numpy as np
import math
from random import random


def xd(X):
    return ((X[0] + 1) ** 2)


def rosenbrock_f(X):
    return sum(
        [
            100 * (X[i + 1] - X[i] ** 2) ** 2 + (X[i] - 1) ** 2
            for i in range(len(X) - 1)
        ],
    )[0]


def rastrigin(x):
    return 10 * len(x) + sum([((xi)**2 - 10 * np.cos(2 * np.pi * (xi))) for xi in x])


class PVS:
    name = "PVS"
    generation = 0

    def __init__(self):
        pass

    # step 1
    def solve(self, fun, PS, FE, DV, LB, UB):
        best_solutions = []
        X = np.random.uniform(LB, UB, (PS, DV))
        r1 = 0
        X = sorted(X, key=lambda x: fun(x), reverse=False)

        best_gen_solution = []
        best_gen_value = math.inf
        for _ in range(FE):
            r2 = np.random.randint(0, PS)
            r3 = np.random.randint(0, PS)

            while r2 == r1:
                r2 = np.random.randint(0, PS)

            while r2 == r3 or r1 == r3:
                r3 = np.random.randint(0, PS)

            X1 = X[r1]
            X2 = X[r2]
            X3 = X[r3]

            r = np.array([r1, r2, r3])

            D = 1 / PS * r
            V = np.random.random() * (1 - D)

            D1, D2, D3 = D
            V1, V2, V3 = V

            x = np.absolute(D3 - D1)
            y = np.absolute(D3 - D2)
            x1 = (V3 * x) / (V1 - V3)
            y1 = (V2 * x) / (V1 - V3)

            V_co = V1 / (V1 - V3)

            if V3 < V1:
                if (y - y1) > x1:
                    new_X1 = X1 + np.random.random() * V_co * (X1 - X3)
                    pass
                else:
                    new_X1 = X1 + np.random.random() * (X1 - X2)
                    pass
            else:
                new_X1 = X1 + np.random.random() * (X3 - X1)
                pass

            new_x1_value = fun(new_X1)
            current_x1_value = fun(X1)

            if new_x1_value < current_x1_value:
                X1 = new_X1
                X[r1] = X1

                if new_x1_value < best_gen_value:
                    best_gen_value = new_x1_value
                    best_gen_solution = X1

            else:
                if current_x1_value < best_gen_value:
                    best_gen_value = current_x1_value
                    best_gen_solution = X1




            for k in range(PS - 1):
                if all(X[k] == X[k + 1]):
                    i = np.random.randint(0, DV)
                    X[k + 1][i] = LB + np.random.random() * (UB - LB)

            r1 += 1
            if r1 == PS or _ == FE - 1:
                r1 = 0
                X = np.random.uniform(LB, UB, (PS, DV))
                X = sorted(X, key=lambda x: fun(x), reverse=False)

                best_solutions.append(best_gen_solution)

                best_gen_solution = []
                best_gen_value = math.inf

        best = sorted(best_solutions, key=lambda x: fun(x), reverse=False)
        return best[0], fun(best[0])


# print(np.array([[n for m in range(3)] for n in range(5)]))

pvc = PVS()
print(pvc.solve(xd, 5, 20, 4, -5.12, 5.12))
