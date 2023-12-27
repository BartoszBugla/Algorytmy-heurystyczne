from typing import Optional
from pydantic import BaseModel, Field


class ParamInfo(BaseModel):
    name: str
    description: str
    upper_bound: float
    lower_bound: float


class AlgorithmMetadata(BaseModel):
    name: str
    params_info: Optional[list[ParamInfo]] = None
