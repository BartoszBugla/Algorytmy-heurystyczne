from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Callable

import numpy as np


class IStateWriter(ABC):
    @abstractmethod
    def save_to_file_state_of_algorithm(self, path: str) -> None:
        pass


class IStateReader(ABC):
    @abstractmethod
    def load_from_file_state_of_algorithm(self, path: str) -> None:
        pass


class IGeneratePDFReport(ABC):
    @abstractmethod
    def generate_pdf_report(self, path: str) -> None:
        pass


class IGenerateTextReport(ABC):
    @abstractmethod
    def generate_text_report(self, path: str) -> str:
        pass


class IOptimizationAlgorithm(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self.params_info: List[ParamInfo] = []

        self.gen_num: int = 0
        self.number_of_evaluation_fitness_function = 0
        self.X: Optional[np.ndarray] = None
        self.Y: Optional[Dict] = None

        self.x_best: Optional[float] = None
        self.f_best: Optional[float] = None

        self.writer: Optional[IStateWriter] = None
        self.reader: Optional[IStateReader] = None
        self.pdf_report_generator: Optional[IGeneratePDFReport] = None
        self.text_report_generator: Optional[IGenerateTextReport] = None

    @abstractmethod
    async def solve(
        self, f: Callable, domain: List[List[float]], parameters: List[float]
    ) -> None:
        pass


@dataclass
class ParamInfo:
    def __init__(
        self, name: str, description: str, upper_boundary: float, lower_boundary: float
    ):
        self.name: str = name
        self.description: str = description
        self.upper_bound: float = upper_boundary
        self.lower_bound: float = lower_boundary

    def __repr__(self):
        return (
            f"{self.name}: {self.description} ({self.lower_bound}, {self.upper_bound})"
        )
