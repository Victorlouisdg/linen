import numpy as np

from linen.path.path import Path


def combine_orientation_and_position_paths(orientation: Path, position: Path) -> Path:
    """Combine an orientation and position path into a pose path.

    Args:
        orientation: The orientation path that returns 3x3 matrices.
        position: The position path.

    Returns:
        The pose path, that returns 4x4 pose matrices.
    """

    def pose(t):
        pose = np.identity(4)
        pose[:3, :3] = orientation(t)
        pose[:3, 3] = position(t)
        return pose

    # TODO maybe enforce/assert that the trajectories are start and end together?
    # Combining two incorrect trajectories has resulted in a bug for me.
    start = min(orientation.start_time, position.start_time)
    end = max(orientation.end_time, position.end_time)

    return Path(pose, start, end)
