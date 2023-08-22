from pydantic import BaseModel


class Statistics(BaseModel):
    min: float
    max: float
    std: float
    mean: float
    m0: float
    m1: float
    m2: float
    m4: float
    tp: float
