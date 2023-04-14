from typing import Callable

import numpy as np

from linen.path.path import Path


def linear_interpolation(a: np.ndarray, b: np.ndarray) -> Callable[[float], np.ndarray]:
    return lambda t: a + t * (b - a)


def linear_path(p0: np.ndarray, p1: np.ndarray) -> Path:
    function = linear_interpolation(p0, p1)
    return Path(function, 0.0, 1.0)


def linear_trajectory(p0: np.ndarray, p1: np.ndarray, speed: float) -> Path:
    """A linear path that you travel at a given constant speed."""
    linear = linear_interpolation(p0, p1)  # domain [0, 1]
    length = np.linalg.norm(p1 - p0)
    duration = length / speed

    def function(t: float) -> np.ndarray:
        return linear(t / duration)  # domain [0, duration]

    return Path(function, 0.0, duration)
