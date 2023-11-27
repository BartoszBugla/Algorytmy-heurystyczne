import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Tester:
    solutions = []

    def __init__(self, solution, samples):
        self.solutions = [solution() for i in range(samples)]
        print("Solutions: ", self.solutions)
        self.y = [x[1] for x in self.solutions]
        print(f"Y: {self.y}")
        self.x = [x[0] for x in self.solutions]
        print(f"X: {self.x}")
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

        return [round(x, 4) for x in best[0]], round(best[1], 3)

    def worst_solution(self):
        worst = max(self.solutions, key=lambda x: x[1])

        return round(worst[1], 3)

    def get_x_std(self):
        return self.df_x.std()

    def get_x_mean(self):
        return self.df_x.mean()

    def get_variation_x(self):
        coefs = list(np.array(self.get_x_std()) / np.array(self.get_x_mean()) * 100)
        return [round(x, 3) for x in coefs]

    def get_variation_y(self):
        return round(self.get_y_std() / self.get_y_mean() * 100, 3)
