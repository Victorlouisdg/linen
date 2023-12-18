from typing import Tuple

from linen.path.path import Path


def split_pose_path(pose_path: Path) -> Tuple[Path, Path]:
    """Split a pose path into an orientation and position path.

    Args:
        pose_path: The pose path, that returns 4x4 pose matrices.

    Returns:
        The orientation path and position path.
    """

    def position(t):
        return pose_path(t)[:3, 3]

    def orientation(t):
        return pose_path(t)[:3, :3]

    position_path = Path(position, pose_path.start_time, pose_path.end_time)
    orientation_path = Path(orientation, pose_path.start_time, pose_path.end_time)
    return orientation_path, position_path
