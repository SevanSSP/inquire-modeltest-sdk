import random
import string
import numpy as np
from typing import Union


def random_bool() -> bool:
    return bool(random.randint(0, 1))


def random_float() -> float:
    return round(random.uniform(0, 100000), 8)


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_lower_short_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=5))


def random_lower_int() -> int:
    return random.randint(10, 15)

def random_int() -> int:
    return random.randint(1000, 9999)


def rounded_compare(number_1: Union[float, np.array], number_2: Union[float, np.array], precision: float):
    return abs((number_1-number_2) / number_1) < precision
