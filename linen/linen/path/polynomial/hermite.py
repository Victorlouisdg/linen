from typing import Callable

import numpy as np

from linen.path.path import Path


# Hermite curve
def hermite_function(p0: np.ndarray, v0: np.ndarray, p1: np.ndarray, v1: np.ndarray) -> Callable[[float], np.ndarray]:
    return (
        lambda t: (2 * t**3 - 3 * t**2 + 1) * p0
        + (t**3 - 2 * t**2 + t) * v0
        + (-2 * t**3 + 3 * t**2) * p1
        + (t**3 - t**2) * v1
    )


def hermite_path(p0: np.ndarray, v0: np.ndarray, p1: np.ndarray, v1: np.ndarray) -> Path:
    function = hermite_function(p0, v0, p1, v1)
    return Path(function, start_time=0.0, end_time=1.0)
