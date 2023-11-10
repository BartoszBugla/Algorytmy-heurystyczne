from abc import ABC, abstractmethod
from typing import Callable

FitnessFunction = Callable[..., float]
