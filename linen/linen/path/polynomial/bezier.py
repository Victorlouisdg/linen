from typing import Callable

import numpy as np

from linen.path.path import Path


# Quadratic Bezier curve
def quadratic_bezier_function(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> Callable[[float], np.ndarray]:
    return lambda t: (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2


def quadratic_bezier_path(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> Path:
    function = quadratic_bezier_function(p0, p1, p2)
    return Path(function, start_time=0.0, end_time=1.0)


# Cubic Bezier curve
def cubic_bezier_function(
    p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray
) -> Callable[[float], np.ndarray]:
    return lambda t: (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3


def cubic_bezier_path(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Path:
    function = cubic_bezier_function(p0, p1, p2, p3)
    return Path(function, start_time=0.0, end_time=1.0)
