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


def sphere_function(x):
    return sum(xi**2 for xi in x)


def beale_function(X):
    x, y = X
    term1 = (1.5 - x + x * y) ** 2
    term2 = (2.25 - x + x * y**2) ** 2
    term3 = (2.625 - x + x * y**3) ** 2
    return term1 + term2 + term3


def bukin_function_n6(X):
    x, y = X
    term1 = 100 * abs(y - 0.01 * x**2) ** 0.5
    term2 = 0.01 * abs(x + 10)
    return term1 + term2
