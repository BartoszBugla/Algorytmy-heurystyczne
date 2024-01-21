import math
from typing import List, Callable, Dict, Optional, TypedDict

import numpy as np
import os
import random

from storage.algorithms.interfaces import (
    IStateReader,
    IStateWriter,
    IGeneratePDFReport,
    IGenerateTextReport,
    IOptimizationAlgorithm,
    ParamInfo,
)

class AlgorithmState(TypedDict):
    IterationNumber: int
    NumberOfEvaluationFitnessFunction: int
    Population: np.ndarray
    Fitness: np.ndarray

class SnakeWriter(IStateWriter):
    def save_to_file_state_of_algorithm(self, path, algorithm_state):
        try:
            with open(path, 'w') as writer:
                writer.write(f"{algorithm_state['IterationNumber']}\n")
                writer.write(f"{algorithm_state['NumberOfEvaluationFitnessFunction']}\n")

                for i in range(len(algorithm_state['Fitness'])):
                    x_str = " ".join(map(str, algorithm_state['Population'][i]))
                    writer.write(f"{x_str} {algorithm_state['Fitness'][i]}\n")

            # Uncomment the next line if you want to print a success message
            # print(f"Plik {path} został pomyślnie zapisany.")
        except Exception as ex:
            print(f"Wystąpił błąd podczas zapisu do pliku: {ex}")

class SnakeReader(IStateReader):
    def load_from_file_state_of_algorithm(self, path: str) -> AlgorithmState:
        x_list = []
        y_list = []

        iteration_number = 0
        number_of_evaluation_fitness_function = 0

        with open(path, 'r') as file:
            iteration_number = int(file.readline().strip())

            # Read the number of fitness function evaluations
            number_of_evaluation_fitness_function = int(file.readline().strip())

            # Read population along with fitness values
            for line in file:
                parts = line.split(' ')

                # Sample data handling - adjust to the actual format
                x = list(map(float, parts[:-1]))
                y = float(parts[-1])

                x_list.append(x)
                y_list.append(y)

        X = np.array(x_list)
        fitness = np.array(y_list)

        return {
            "IterationNumber": iteration_number,
            "NumberOfEvaluationFitnessFunction": number_of_evaluation_fitness_function,
            "Population": X,
            "Fitness": fitness
        }

class SnakeGeneratePDFReport(IGeneratePDFReport):
    pass

class snake(IOptimizationAlgorithm):
    def __init__(self):
        super().__init__("Snake")

        self.params_info: List[ParamInfo] = [
            ParamInfo("T", "Liczba iteracji", 200, 10),
            ParamInfo("N", "Rozmiar populacji", 200, 10),
        ]
        self.writer: SnakeWriter = SnakeWriter()
        self.reader: SnakeReader = SnakeReader()

    def solve(self, fitness_function: Callable, domain, parameters: List[float]) -> List[float]:
        domain = np.array(domain)
        print(parameters)
        dim = domain.shape[1]

        self.XBest = np.zeros(dim)
        self.FBest = 0.0
        self.number_of_evaluation_fitness_function = 0

        xmin = domain[0, :]
        xmax = domain[1, :]

        T, N = [int(i) for i in parameters]
        tStart = 1

        rnd = random.Random()
        X = np.zeros((N, dim))
        
        fitness = np.zeros(N)

        if os.path.exists("snake_state.txt"):
            algorithm_state = self.reader.load_from_file_state_of_algorithm("snake_state.txt")

            tStart = algorithm_state["IterationNumber"] + 1
            self.number_of_evaluation_fitness_function = algorithm_state["NumberOfEvaluationFitnessFunction"]
            X = algorithm_state["Population"]
            fitness = algorithm_state["Fitness"]
        else:
            self.number_of_evaluation_fitness_function = 0

            # Initialize snake swarm and calculate fitness of each snake
            for i in range(N):
                X[i] = xmin + rnd.random() * (xmax - xmin)
                fitness[i] = fitness_function(X[i])
                self.number_of_evaluation_fitness_function += 1

        # print(tStart)

        # for x in fitness:
        #     print(x)

        # Constant variables
        vecflag = [1, -1]
        treshold1 = 0.25
        treshold2 = 0.6
        c1 = 0.5
        c2 = 0.05
        c3 = 2

        # Get food position (Xfood)
        bestSnake_fitValue = np.min(fitness)
        bestSnake_fitValue_index = np.where(fitness == bestSnake_fitValue)[0][0]
        self.XBest = X[bestSnake_fitValue_index].copy()

        # Divide the swarm
        Nm = N // 2
        Nf = N - Nm
        Xm = X[:Nm].copy()  # males
        Xf = X[Nm:].copy()  # females
        male_fitness = fitness[:Nm].copy()
        female_fitness = fitness[Nm:].copy()

        
        

        # Get best male
        bestMale_fitValue = np.min(male_fitness)
        bestMale_fitValue_index = np.where(male_fitness == bestMale_fitValue)[0][0]
        XBestMale = Xm[bestMale_fitValue_index].copy()

        # Get best female (same as male)
        bestFemale_fitValue = np.min(female_fitness)
        bestFemale_fitValue_index = np.where(female_fitness == bestFemale_fitValue)[0][0]
        XBestFemale = Xf[bestFemale_fitValue_index].copy()

        Xnewm = np.zeros((Nm, dim))
        Xnewf = np.zeros((Nf, dim))

        for t in range(tStart, T + 1):
            # Calculate temperature
            Temp = math.exp(-t / T)
            # Calculate food quantity
            Q = c1 * math.exp((t - T) / T)
            if Q > 1:
                Q = 1

            if Q < treshold1:
                # Exploration phase (no food)
                # Every snake searches for food and goes to a random position

                # For males
                for i in range(Nm):
                    randmid = int(Nm * rnd.random())
                    Xrandm = Xm[randmid].copy()
                    flagid = int(2 * rnd.random())
                    flag = vecflag[flagid]
                    Am = math.exp(-male_fitness[randmid] / (male_fitness[i] + np.finfo(float).eps))
                    Xnewm[i] = Xrandm + flag * c2 * Am * ((xmax - xmin) * rnd.random() + xmin)

                # For females
                for i in range(Nf):
                    randfid = int(Nf * rnd.random())
                    Xrandf = Xf[randfid].copy()
                    flagid = int(2 * rnd.random())
                    flag = vecflag[flagid]
                    Af = math.exp(-female_fitness[randfid] / (female_fitness[i] + np.finfo(float).eps))
                    Xnewf[i] = Xrandf + flag * c2 * Af * ((xmax - xmin) * rnd.random() + xmin)
            else:
                # Exploitation phase (food exists)
                if Temp > treshold2:
                    # Hot
                    # Snakes go to the food

                    # For males
                    for i in range(Nm):
                        flagid = int(2 * rnd.random())
                        flag = vecflag[flagid]
                        Xnewm[i] = self.XBest + flag * c3 * Temp * rnd.random() * (self.XBest - Xm[i])

                    # For females
                    for i in range(Nf):
                        flagid = int(2 * rnd.random())
                        flag = vecflag[flagid]
                        Xnewf[i] = self.XBest + flag * c3 * Temp * rnd.random() * (self.XBest - Xf[i])
                else:  # Cold
                    if rnd.random() > 0.6:
                        # Fight

                        # For males
                        for i in range(Nm):
                            Fm = math.exp(-bestFemale_fitValue / (male_fitness[i] + np.finfo(float).eps))
                            Xnewm[i] = Xm[i] + c3 * Fm * rnd.random() * (Q * XBestFemale - Xm[i])

                        # For females
                        for i in range(Nf):
                            Ff = math.exp(-bestMale_fitValue / (female_fitness[i] + np.finfo(float).eps))
                            Xnewf[i] = Xf[i] + c3 * Ff * rnd.random() * (Q * XBestMale - Xf[i])
                    else:
                        # Mating

                        # For males
                        for i in range(Nm):
                            Mm = math.exp(-female_fitness[i] / (male_fitness[i] + np.finfo(float).eps))
                            Xnewm[i] = Xm[i] + c3 * Mm * rnd.random() * (Q * Xf[i] - Xm[i])

                        # For females
                        for i in range(Nf):
                            Mf = math.exp(-male_fitness[i] / (female_fitness[i] + np.finfo(float).eps))
                            Xnewf[i] = Xf[i] + c3 * Mf * rnd.random() * (Q * Xm[i] - Xf[i])

                        # Randomize if egg hatches
                        flagid = int(2 * rnd.random())
                        egg = vecflag[flagid]

                        # Check if egg is there or not
                        if egg == 1:
                            # Get worst male and female
                            worstMale_fitValue_index = np.argmax(male_fitness)
                            worstFemale_fitValue_index = np.argmax(female_fitness)
                            # Replace them
                            Xnewm[worstMale_fitValue_index] = xmin + rnd.random() * (xmax - xmin)
                            Xnewf[worstFemale_fitValue_index] = xmin + rnd.random() * (xmax - xmin)

            for i in range(Nm):
                for j in range(dim):
                    if Xnewm[i, j] > xmax[j]:
                        Xnewm[i, j] = xmax[j]
                    if Xnewm[i, j] < xmin[j]:
                        Xnewm[i, j] = xmin[j]

                y = fitness_function(Xnewm[i])
                self.number_of_evaluation_fitness_function += 1
                if y < male_fitness[i]:
                    male_fitness[i] = y
                    Xm[i] = Xnewm[i].copy()

            for i in range(Nf):
                for j in range(dim):
                    if Xnewf[i, j] > xmax[j]:
                        Xnewf[i, j] = xmax[j]
                    if Xnewf[i, j] < xmin[j]:
                        Xnewf[i, j] = xmin[j]

                y = fitness_function(Xnewf[i])
                self.number_of_evaluation_fitness_function += 1
                if y < female_fitness[i]:
                    female_fitness[i] = y
                    Xf[i] = Xnewf[i].copy()

            newBestMale_fitValue = np.min(male_fitness)
            newBestMale_fitValue_index = np.where(male_fitness == newBestMale_fitValue)[0][0]

            newBestFemale_fitValue = np.min(female_fitness)
            newBestFemale_fitValue_index = np.where(female_fitness == newBestFemale_fitValue)[0][0]

            if newBestMale_fitValue < bestMale_fitValue:
                XBestMale = Xm[newBestMale_fitValue_index].copy()
                bestMale_fitValue = newBestMale_fitValue

            if newBestFemale_fitValue < bestFemale_fitValue:
                XBestFemale = Xf[newBestFemale_fitValue_index].copy()
                bestFemale_fitValue = newBestFemale_fitValue

            if bestMale_fitValue < bestFemale_fitValue:
                self.FBest = bestMale_fitValue
                self.XBest = XBestMale.copy()
            else:
                self.FBest = bestFemale_fitValue
                self.XBest = XBestFemale.copy()

            X[:Nm, :] = Xm.copy()
            X[Nm:, :] = Xf.copy()

            fitness[:Nm] = male_fitness.copy()
            fitness[Nm:] = female_fitness.copy()

            algorithm_state = {
                "IterationNumber": t,
                "NumberOfEvaluationFitnessFunction": self.number_of_evaluation_fitness_function,
                "Population": X.copy(),
                "Fitness": fitness.copy()
            }

            self.writer.save_to_file_state_of_algorithm("snake_state.txt", algorithm_state)
        self.x_best = self.XBest
        self.f_best = self.FBest
        if os.path.exists("snake_state.txt"):
            os.remove("snake_state.txt")

        return self.XBest