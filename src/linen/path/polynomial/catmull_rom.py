from typing import List

import numpy as np

from linen.path.concatenate import concatenate_trajectories
from linen.path.path import Path
from linen.path.polynomial.hermite import hermite_path


def catmull_rom_path(points: List[np.ndarray]) -> Path:
    tangents = []
    for i in range(len(points)):
        if i == 0:
            tangents.append(points[i + 1] - points[i])
        elif i == len(points) - 1:
            tangents.append(points[i] - points[i - 1])
        else:
            tangents.append(0.5 * (points[i + 1] - points[i - 1]))

    hermite_paths = []
    for i in range(len(points) - 1):
        hermite_paths.append(hermite_path(points[i], tangents[i], points[i + 1], tangents[i + 1]))

    catmull_rom_path = concatenate_trajectories(hermite_paths)
    return catmull_rom_path
