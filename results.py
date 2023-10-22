import matplotlib.pyplot as plt
import numpy as np


class Tester:
    solutions = []

    def __init__(self, fun, samples):
        self.solutions = [fun() for i in range(samples)]
        self.y = [x[1] for x in self.solutions]
        self.x = [x[0] for x in self.solutions]
        self.samples_count = samples

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
