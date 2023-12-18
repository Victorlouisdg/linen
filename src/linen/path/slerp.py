from typing import List

import numpy as np
from scipy.spatial.transform import Rotation, Slerp

from linen.path.path import Path


def slerp_trajectory(times: List[float], orientations: List[np.ndarray]) -> Path:
    """
    Create a path of interpolated orientations. At least two orientations are required.
    The amount of orientations must equal the amount of times.

    Args:
        times: The times at which the orientations are defined.
        orientations: The orientations at the given times.

    Returns:
        The path of interpolated orientations.
    """
    orientations_scipy = Rotation.from_matrix(np.array(orientations))
    slerp = Slerp(times, orientations_scipy)
    return Path(lambda t: slerp(t).as_matrix(), times[0], times[-1])
