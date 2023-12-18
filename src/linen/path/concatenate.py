from typing import List

import numpy as np

from linen.path.path import Path


def concatenate_trajectories(trajectories: List[Path]) -> Path:
    durations = [trajectory.duration for trajectory in trajectories]
    functions = [trajectory.function for trajectory in trajectories]

    def concatenated_functions(t: float) -> np.ndarray:
        for function, duration in zip(functions, durations):
            if t <= duration:
                return function(t)
            t -= duration  # go to next trajectory
        return function(duration)  # if we get here, return last point

    return Path(concatenated_functions, 0.0, sum(durations))
