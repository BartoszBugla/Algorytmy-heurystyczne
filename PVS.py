import numpy as np
import math
from random import random


def xD_f(X):
    return X[0] + X[1] + X[2]


def rosenbrock_f(X):
    return sum(
        [
            100 * (X[i + 1] - X[i] ** 2) ** 2 + (X[i] - 1) ** 2
            for i in range(len(X) - 1)
        ],
    )[0]


def restrigin_f(X):
    return (
        10
        * len(X)
        * sum([X[i] ** 2 - 10 * math.cos(2 * math.pi * X[i]) for i in range(len(X))])[0]
    )


class PVS:
    name = "PVS"
    generation = 0

    def __init__(self):
        pass

    # step 1
    def solve(self, fun, ps, noge=None, fe=1, dv=1, lb=-5.12, ub=5.12) -> float:
        # step 2
        X = np.random.uniform(lb, ub, size=(ps, dv))
        print(
            "\n".join(["    ".join(["{:4}".format(item) for item in row]) for row in X])
        )

        # step 3
        for _ in range(fe):
            r1 = 0
            r2 = 0
            r3 = 0

            while r2 == 0 or r2 == r1:
                r2 = math.floor(random() * ps)

            while r3 == 0 or r3 == r1:
                r3 = math.floor(random() * ps)

            r1 = X[r1]
            r2 = X[r2]
            r3 = X[r3]

            print("r1: ", r1, " r2: ", r2, " r3: ", r3)

            # # step 4
            d1 = np.absolute(1 / ps * r1)
            d2 = np.absolute(1 / ps * r2)
            d3 = np.absolute(1 / ps * r3)

            R1 = random()
            R2 = random()
            R3 = random()

            v1 = R1 * (1 - d1)
            v2 = R2 * (1 - d2)
            v3 = R3 * (1 - d3)

            print("v1: ", v1, "v2: ", v2, "v3: ", v3)
            print("d1: ", d1, "d2: ", d2, "d3: ", d3)
            # # step 5
            x = np.absolute(d3 - d1)
            y = np.absolute(d3 - d2)
            x1 = (v3 * x) / (v1 - v3)
            y1 = v2 * x * (v1 - v3)

            print("x: ", x, "y: ", y, "x1:", x1, "y: ", y1)
            # step 6
            v_co = v1 / v1 - v3
            new_X = []

            if v3 < v1:
                if (y - y1) > x1:
                    new_X = [
                        X[k]
                        + v_co
                        * random()
                        * (X[k][math.floor(d1 * dv) - math.floor(d3 * dv)])
                        for k in range(ps)
                    ]

                else:
                    new_X = [
                        X[k]
                        + v_co
                        * random()
                        * (X[k][math.floor(d1 * dv) - math.floor(d2 * dv)])
                        for k in range(ps)
                    ]

            else:
                new_X = [
                    X[k]
                    + v_co
                    * random()
                    * (X[k][math.floor(d3 * dv) - math.floor(d1 * dv)])
                    for k in range(ps)
                ]

            print("wartość funkcji: ", fun(X), "X", X)
            if fun(new_X) < fun(X):
                X = new_X


# print(np.array([[n for m in range(3)] for n in range(5)]))

pvc = PVS()
pvc.solve(xD_f, 15, fe=1)
