from typing import Callable

import numpy as np

from linen.path.combine import combine_orientation_and_position_paths
from linen.path.constant import constant_trajectory
from linen.path.path import Path
from linen.path.slerp import slerp_trajectory


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


def linear_constant_orientation_trajectory(p0: np.ndarray, p1: np.ndarray, orientation: np.ndarray, speed: float):
    """A linear position trajectory where the orientation is constant."""
    position_trajectory = linear_trajectory(p0, p1, speed)
    orientation_trajectory = constant_trajectory(orientation, position_trajectory.duration)
    return combine_orientation_and_position_paths(orientation_trajectory, position_trajectory)


def linear_slerp_trajectory(pose0: np.ndarray, pose1: np.ndarray, speed: float) -> Path:
    """A linear position trajectory where the orientation is interpolated using slerp."""

    p0, p1 = pose0[:3, 3], pose1[:3, 3]
    position_trajectory = linear_trajectory(p0, p1, speed)

    orientations = [pose0[:3, :3], pose1[:3, :3]]
    times = [0.0, position_trajectory.duration]
    orientation_trajectory = slerp_trajectory(times, orientations)

    pose_trajectory = combine_orientation_and_position_paths(orientation_trajectory, position_trajectory)
    return pose_trajectory
