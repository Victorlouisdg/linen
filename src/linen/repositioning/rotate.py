from typing import Tuple

import numpy as np

from linen.path.circular_arc import circular_arc_trajectory
from linen.path.path import Path


def rotate_trajectories(pose0: np.ndarray, pose1: np.ndarray, angle: float = np.pi / 2) -> Tuple[Path, Path]:
    """A dual arm motion where two grippers rotate around their common center. This is useful for example when you've
    folded a towel once, and want to fold it a second time with fold arcs in the same direction.

    Args:
        pose0: Start tcp pose of one of the arms.
        pose1: Start tcp pose of the other arm
        angle: The amount to rotate along the vertical axis. Positive angles are counterclockwise.

    Returns:
        _description_
    """
    rotate_axis = np.array([0, 0, 1])

    # TODO: Quick fix for negative end causing problems. This should be handled in circular_arc_trajectory
    if angle < 0:
        angle = -angle
        rotate_axis = -rotate_axis

    center = (pose0[:3, 3] + pose1[:3, 3]) / 2
    trajectory0 = circular_arc_trajectory(pose0, center, rotate_axis, angle, speed=0.1)
    trajectory1 = circular_arc_trajectory(pose1, center, rotate_axis, angle, speed=0.1)
    return trajectory0, trajectory1
