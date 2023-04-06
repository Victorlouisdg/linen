from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class Path:
    """A path is a function that maps points from its scalar domain [start_time, end_time] to values.
    These values can be many things e.g. a 1D, 2D, 3D point, a rotation, a pose, a vector of 6 joint states etc.

    A trajectory is path where the domain is interpreted as time. For this reason, we don't make a distinct class for
    trajectories. However, we follow the convention that the start of a trajectory is 0 and the end is duration,
    i.e. its domain is [0, duration].

    The reason using a class for Path vs simply representating them as functions + domain is that is becomes cumbersome
    to keep track of the domains/durations. It is also bug-prone because you can easily evaluate a path outside of its
    domain.

    However, we do not make seperate classes for each type of path (e.g. a linear, a quadratic bezier, circular etc.)
    as that would make composing and transforming paths more complex. We prefer the pattern with builder_functions e.g.
    linear_path, quadratic_bezier_path, etc. that return a Path with the correct path function and domain.
    """

    function: Callable[[float], np.ndarray]
    start_time: float
    end_time: float

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    @property
    def start(self) -> np.ndarray:
        return self.function(self.start_time)

    @property
    def end(self) -> np.ndarray:
        return self.function(self.end_time)

    def __call__(self, t: float) -> np.ndarray:
        return self.function(t)

    # TODO considers adding either convencience (holding value) or assert for sampling outside of domain
    # TODO consider distinguishing between PositionPath, OrientationPath and PosePath e.g. for visualization
    # TODO how to handle joint paths
