from abc import ABC


class ParamInfo(ABC):
    name: str
    description: str
    upper_boundary: float
    lower_boundary: float
