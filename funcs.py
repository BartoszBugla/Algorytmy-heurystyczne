import numpy as np


def rastrigin(x):
    return 10 * len(x) + sum([((xi) ** 2 - 10 * np.cos(2 * np.pi * (xi))) for xi in x])


def base(x):
    return x[0] * x[1]


def rosenbrock(x):
    n = len(x)
    result = 0
    for i in range(n - 1):
        result += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
    return result


def xd(X):
    return (X[0] + 1) ** 2 - 1
