import numpy as np

from interfaces import (
    IStateReader,
    IStateWriter,
    IGeneratePDFReport,
    IGenerateTextReport,
    IOptimizationAlgorithm,
)

from typing import Optional, List, Dict, TypedDict

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

# Example usage:
# state_writer = SnakeWriter()
# algorithm_state = {
#     "IterationNumber": 1,
#     "NumberOfEvaluationFitnessFunction": 100,
#     "Population": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
#     "Fitness": [10.0, 20.0]
# }
# state_writer.save_to_file_state_of_algorithm("state.txt", algorithm_state)
