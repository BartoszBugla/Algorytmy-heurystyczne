import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Tester:
    solutions = []

    def __init__(self, solution, samples):
        self.solutions = [solution() for i in range(samples)]
        self.y = [x[1] for x in self.solutions]
        self.x = [x[0] for x in self.solutions]
        self.samples_count = samples
        self.df_x = pd.DataFrame(self.x)
        self.df_y = pd.DataFrame(self.y)

    def get_y_mean(self):
        return np.mean(self.y)

    def get_y_std(self):
        return np.std(self.y)

    def draw_2D_x_plot(self):
        plt.scatter([x[0] for x in self.x], [x[1] for x in self.x])
        plt.show()

    def draw_y_plot(self):
        plt.scatter(self.y, self.y)
        plt.show()

    def best_solution(self):
        best = min(self.solutions, key=lambda x: x[1])
        return list(best[0]), best[1]

    def get_std_params(self):
        return list(self.df_x.std())


