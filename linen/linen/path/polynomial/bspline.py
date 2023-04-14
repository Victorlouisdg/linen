from typing import Callable

import numpy as np

from linen.path.path import Path

# Note that SciPy also has a BSpline class we could use.
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BSpline.html


def bspline_function(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Callable[[float], np.ndarray]:
    characteristic_matrix = np.array(
        [
            [1, 4, 1, 0],
            [-3, 0, 3, 0],
            [3, -6, 3, 0],
            [-1, 3, -3, 1],
        ],
        dtype=np.float64,
    )
    characteristic_matrix /= 6.0

    def bspline(t):
        t_vector = np.array([1, t, t**2, t**3])
        return t_vector @ characteristic_matrix @ np.array([p0, p1, p2, p3])

    return bspline


def bspline_path(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Path:
    function = bspline_function(p0, p1, p2, p3)
    return Path(function, start_time=0.0, end_time=1.0)
