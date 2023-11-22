def __main__(X):
    x, y = X
    term1 = 100 * abs(y - 0.01 * x**2) ** 0.5
    term2 = 0.01 * abs(x + 10)
    return term1 + term2
