from linen.path.reparametrization.speed import scale_speed


def synchronize(trajectory0, trajectory1):
    """Slow down one the trajectories to match the duration of the other."""
    duration0 = trajectory0.duration
    duration1 = trajectory1.duration

    if duration0 > duration1:
        factor = duration1 / duration0
        trajectory1 = scale_speed(trajectory1, factor)
    elif duration1 > duration0:
        factor = duration0 / duration1
        trajectory0 = scale_speed(trajectory0, factor)

    return trajectory0, trajectory1
