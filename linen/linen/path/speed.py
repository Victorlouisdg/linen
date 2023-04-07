from linen.path.path import Path


def scale_speed(trajectory: Path, factor: float) -> Path:
    """Scale the speed of a trajectory by a given factor. Factors > 1.0 speed up the trajectory, factors < 1.0 slow it down.

    Args:
        trajectory: The trajectory to scale. Must start at t=0.0.
        factor: The factor to scale the speed by.

    Returns:
        The scaled trajectory.
    """
    return Path(
        lambda t: trajectory(t * factor),
        start_time=0.0,
        end_time=trajectory.end_time / factor,
    )
