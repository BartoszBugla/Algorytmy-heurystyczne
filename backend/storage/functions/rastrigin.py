import numpy as np


def __main__(x):
    return 10 * len(x) + sum([((xi) ** 2 - 10 * np.cos(2 * np.pi * (xi))) for xi in x])
