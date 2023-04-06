import numpy as np
from syncloth.paths.path import Path


def constant_trajectory(value: np.ndarray, duration: float) -> Path:
    def constant_function(t: float) -> np.ndarray:
        return value

    return Path(constant_function, 0.0, duration)
