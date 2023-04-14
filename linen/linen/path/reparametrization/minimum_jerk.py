from linen.path.path import Path


def minimum_jerk_function(t: float):
    """Minimum jerk function for t in [0, 1]"""
    return 10 * (t**3) - 15 * (t**4) + 6 * (t**5)


def minimum_jerk_path() -> Path:
    return Path(minimum_jerk_function, start_time=0.0, end_time=1.0)
